from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User

from .models import Site, Floor, Language, CustomUser, Projects, Teams
from .views import *


class SiteModelTest(TestCase):
    def setUp(self):
        Site.objects.create(code="szz", name="Szczecin")
        Site.objects.create(
            code="waw",
            name="Warsaw",
            address="Central Street",
            city="Warsaw",
            country="Poland",
            postal_code="00-001",
        )

    def test_site_creation(self):
        szczecin = Site.objects.get(code="szz")
        warsaw = Site.objects.get(code="waw")
        self.assertEqual(szczecin.name, "Szczecin")
        self.assertEqual(warsaw.city, "Warsaw")

    def test_optional_fields(self):
        warsaw = Site.objects.get(code="waw")
        self.assertEqual(warsaw.address, "Central Street")
        self.assertIsNone(Site.objects.get(code="szz").address)

    def test_str_representation(self):
        szczecin = Site.objects.get(code="szz")
        warsaw = Site.objects.get(code="waw")
        self.assertEqual(str(szczecin), "Szczecin")
        self.assertEqual(str(warsaw), "Warsaw")


class FloorModelTest(TestCase):
    def setUp(self):
        self.szczecin = Site.objects.create(code="szz", name="Szczecin")
        self.warsaw = Site.objects.create(code="waw", name="Warsaw")
        Floor.objects.create(number=1, name="First Floor", site=self.szczecin)
        Floor.objects.create(number=2, name="Second Floor", site=self.warsaw)

    def test_floor_creation(self):
        first_floor = Floor.objects.get(number=1, site=self.szczecin)
        second_floor = Floor.objects.get(number=2, site=self.warsaw)
        self.assertEqual(first_floor.name, "First Floor")
        self.assertEqual(second_floor.site, self.warsaw)

    def test_str_representation(self):
        first_floor = Floor.objects.get(number=1, site=self.szczecin)
        second_floor = Floor.objects.get(number=2, site=self.warsaw)
        self.assertEqual(str(first_floor), "First Floor (Floor 1) at Szczecin")
        self.assertEqual(str(second_floor), "Second Floor (Floor 2) at Warsaw")

    def test_relationship_with_site(self):
        first_floor = Floor.objects.get(number=1, site=self.szczecin)
        self.assertEqual(first_floor.site.name, "Szczecin")


class LanguageModelTest(TestCase):
    def setUp(self):
        Language.objects.create(code="eng", name="English")

    def test_language_creation(self):
        language = Language.objects.get(code="eng")
        self.assertEqual(language.name, "English")

    def test_str_representation(self):
        language = Language.objects.get(code="eng")
        self.assertEqual(str(language), "English (eng)")


class ProjectsModelTest(TestCase):
    def setUp(self):
        eng_language = Language.objects.create(code="eng", name="English")

        self.manager_user = CustomUser.objects.create(
            username="manager1", is_manager=True, language=eng_language
        )

        self.project1 = Projects.objects.create(
            name="Project1", description="Project1 description"
        )
        self.project1.managers.add(self.manager_user)

        Projects.objects.create(name="Project2", description="")  # Empty description
        Projects.objects.create(name="Project3")  # No description provided

    def test_project_creation_with_full_details(self):
        project = Projects.objects.get(name="Project1")
        self.assertEqual(project.description, "Project1 description")
        self.assertIn(self.manager_user, project.managers.all())

    def test_project_creation_with_empty_description(self):
        project = Projects.objects.get(name="Project2")
        self.assertEqual(project.description, "")

    def test_project_creation_without_description(self):
        project = Projects.objects.get(name="Project3")
        self.assertIsNone(project.description)

    def test_str_representation(self):
        project1 = Projects.objects.get(name="Project1")
        project2 = Projects.objects.get(name="Project2")
        project3 = Projects.objects.get(name="Project3")
        self.assertEqual(str(project1), "Project1")
        self.assertEqual(str(project2), "Project2")
        self.assertEqual(str(project3), "Project3")


class TeamsModelTest(TestCase):
    def setUp(self):
        self.project = Projects.objects.create(
            name="Project1", description="Project1 description"
        )

        self.language = Language.objects.create(code="eng", name="English")

        self.team_lead_user = CustomUser.objects.create(
            username="teamlead", is_team_lead=True, language=self.language
        )

        # Create a team
        self.team = Teams.objects.create(
            name="Team1",
            description="Team1 Description",
            project=self.project,
            team_lead=self.team_lead_user,
        )
        self.team.languages.add(self.language)

    def test_teams_creation_based_on_name(self):
        self.assertEqual(self.team.name, "Team1")
        self.assertEqual(self.team.description, "Team1 Description")
        self.assertIn(self.language, self.team.languages.all())

    def test_str_representation(self):
        self.assertEqual(str(self.team), "Team1")

    def test_team_lead_assignment(self):
        self.assertEqual(self.team.team_lead, self.team_lead_user)


# ==================== Views ====================


class StaffRoleTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.site = Site.objects.create(code="szz", name="Szczecin")
        self.floor = Floor.objects.create(number=1, name="First Floor", site=self.site)
        self.language = Language.objects.create(code="eng", name="English")

        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="top_secret",
            site=self.site,
            language=self.language,
            contract="civil",
        )

    def create_user_with_role(self, **kwargs):
        unique_username = kwargs.get("username", "user") + "_test"

        return CustomUser.objects.create_user(
            username=unique_username,
            email=kwargs.get("email", f"{unique_username}@example.com"),
            password="top_secret",
            site=self.site,
            language=self.language,
            contract="civil",
            is_superuser=kwargs.get("is_superuser", False),
            is_manager=kwargs.get("is_manager", False),
            is_team_lead=kwargs.get("is_team_lead", False),
            is_administrator=kwargs.get("is_administrator", False),
        )

    def test_manage_staff_classifier_superuser(self):
        # Superuser is also an administrator. There is no other website for administrators.
        superuser = self.create_user_with_role(username="superuser", is_superuser=True)
        request = self.factory.get("/manage-staff/")
        request.user = superuser

        response = manage_staff_classifier(request)
        self.assertEqual(response.url, "manage-staff/admin/")
        self.assertEqual(response.status_code, 302)

    def test_manage_staff_classifier_manager(self):
        manager = self.create_user_with_role(username="manager", is_manager=True)
        request = self.factory.get("/manage-staff/")
        request.user = manager

        response = manage_staff_classifier(request)
        self.assertEqual(response.url, "manage-staff/manager/")
        self.assertEqual(response.status_code, 302)

    def test_manage_staff_classifier_team_lead(self):
        team_lead = self.create_user_with_role(username="teamlead", is_team_lead=True)
        request = self.factory.get("/manage-staff/")
        request.user = team_lead

        response = manage_staff_classifier(request)
        self.assertEqual(response.url, "manage-staff/team-leader/")
        self.assertEqual(response.status_code, 302)

    def test_manage_staff_classifier_employee(self):
        # TODO: redirect to employee page
        pass

    def test_manage_staff_unauthenticated(self):
        request = self.factory.get("/manage-staff/")
        request.user = AnonymousUser()

        response = manage_staff_classifier(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        self.assertIn("next=/manage-staff/", response.url)

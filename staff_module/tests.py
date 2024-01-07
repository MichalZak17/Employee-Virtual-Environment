from django.test import TestCase
from .models import Site, Floor, Language, CustomUser, Projects, Teams


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
        Projects.objects.create(name="Project1", description="Project1 description")
        Projects.objects.create(name="Project2", description="")  # Empty description
        Projects.objects.create(name="Project3")  # No description provided

    def test_project_creation_with_full_details(self):
        project = Projects.objects.get(name="Project1")
        self.assertEqual(project.description, "Project1 description")

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
        self.site = Site.objects.create(code="szz", name="Szczecin")
        self.team_lead_user = CustomUser.objects.create(
            username="teamlead",
            language=self.language,
            site=self.site,
            is_team_lead=True,
        )
        self.team_member_user = CustomUser.objects.create(
            username="user1", language=self.language, site=self.site
        )
        self.team = Teams.objects.create(
            name="Team1",
            description="Team1 Description",
            project=self.project,
            team_lead=self.team_lead_user,
        )
        self.team.languages.add(self.language)
        self.team.members.add(self.team_member_user)

    def test_teams_creation_based_on_name(self):
        self.assertEqual(self.team.name, "Team1")
        self.assertEqual(self.team.description, "Team1 Description")
        self.assertIn(self.team_member_user, self.team.members.all())
        self.assertIn(self.language, self.team.languages.all())

    def test_str_representation(self):
        self.assertEqual(str(self.team), "Team1")

    def test_team_lead_assignment(self):
        self.assertEqual(self.team.team_lead, self.team_lead_user)

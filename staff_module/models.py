from django.db import models
from django.contrib.auth.models import AbstractUser


class Site(models.Model):
    """
    Represents a site in the organization.

    Attributes:
        code (str): The code of the site.
        name (str): The name of the site.
        address (str): The address of the site.
        city (str): The city where the site is located.
        country (str): The country where the site is located.
        postal_code (str): The postal code of the site.
    """

    code = models.CharField(max_length=3, primary_key=True, verbose_name="Site Code")
    name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Site Name"
    )
    address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Address"
    )
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="City")
    country = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Country"
    )
    postal_code = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Postal Code"
    )

    def __str__(self):
        return self.name


class Floor(models.Model):
    """
    Represents a floor in a building.

    Attributes:
        number (int): The floor number.
        name (str): The name of the floor.
        site (Site): The site to which the floor belongs.
    """

    number = models.IntegerField(default=1, verbose_name="Floor Number")
    name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Floor Name"
    )
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="floors", verbose_name="Site"
    )

    def __str__(self):
        return f"{self.name} (Floor {self.number}) at {self.site}"


class Language(models.Model):
    code = models.CharField(
        max_length=3, primary_key=True, verbose_name="Language Code"
    )
    name = models.CharField(max_length=100, verbose_name="Language Name")

    def __str__(self):
        return f"{self.name} ({self.code})"


class CustomUser(AbstractUser):
    """
    Represents a custom user in the system.

    Attributes:
        language (ForeignKey): The language preference of the user.
        site (ForeignKey): The site where the user is located.
        contract (CharField): The type of contract the user has.
        is_manager (BooleanField): Indicates if the user is a manager.
        is_team_lead (BooleanField): Indicates if the user is a team lead.
        is_administrator (BooleanField): Indicates if the user is an administrator.
        office_floors (ManyToManyField): The office floors assigned to the user.
    """

    USER_CONTRACT_CHOICES = [("civil", "Civil"), ("labour", "Labour"), ("b2b", "B2B")]

    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        default="eng",
        verbose_name="Language",
    )
    site = models.ForeignKey(
        Site, on_delete=models.SET_NULL, null=True, verbose_name="Site"
    )
    contract = models.CharField(
        max_length=10,
        choices=USER_CONTRACT_CHOICES,
        default="civil",
        verbose_name="Contract Type",
    )
    is_manager = models.BooleanField(default=False, verbose_name="Is Manager")
    is_team_lead = models.BooleanField(default=False, verbose_name="Is Team Lead")
    is_administrator = models.BooleanField(
        default=False, verbose_name="Is Administrator"
    )
    office_floors = models.ManyToManyField(
        Floor, blank=True, null=True, verbose_name="Office Floors"
    )

    def __str__(self):
        return self.username


class Projects(models.Model):
    """
    Represents a project in the system.

    Attributes:
        name (str): The name of the project.
        description (str): The description of the project.
        client (str): The client of the project.
        managers (QuerySet): The managers of the project.
    """

    name = models.CharField(max_length=100, verbose_name="Project Name")
    description = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Project Description"
    )
    client = models.CharField(max_length=100, verbose_name="Client")
    managers = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name="managed_projects",
        verbose_name="Project Managers",
    )

    def __str__(self):
        return self.name


class Teams(models.Model):
    """
    Represents a team in the organization.

    Attributes:
        name (str): The name of the team.
        description (str): The description of the team.
        project (Projects): The project associated with the team.
        team_lead (CustomUser): The team lead for the team.
        languages (QuerySet): The languages used by the team.
    """

    name = models.CharField(max_length=100, verbose_name="Team Name")
    description = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name="Team Description"
    )
    project = models.ForeignKey(
        Projects, on_delete=models.CASCADE, related_name="teams", verbose_name="Project"
    )
    team_lead = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, verbose_name="Team Lead"
    )
    languages = models.ManyToManyField(
        Language, blank=True, null=True, verbose_name="Languages"
    )

    def __str__(self):
        return self.name

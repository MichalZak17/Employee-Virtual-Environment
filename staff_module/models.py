from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_LANGUAGE_CHOICES = [
        ("eng", "English"),
        ("fre", "French"),
        ("ger", "German"),
        ("ita", "Italian"),
        ("spa", "Spanish"),
    ]

    USER_SITE_CHOICES = [
        ("szz", "SZZ"),
        ("kat", "KAT"),
    ]

    USER_CONTRACT_CHOICES = [("civil", "Civil"), ("labour", "Labour")]

    user_workday = models.IntegerField(default=0)

    user_language = models.CharField(
        max_length=3, choices=USER_LANGUAGE_CHOICES, default="eng"
    )

    user_site = models.CharField(max_length=3, choices=USER_SITE_CHOICES, default="szz")

    user_contract = models.CharField(
        max_length=6, choices=USER_CONTRACT_CHOICES, default="civil"
    )

    user_is_manager = models.BooleanField(default=False)

    user_is_team_lead = models.BooleanField(default=False)

    user_is_administrator = models.BooleanField(default=False)

    user_team = models.ForeignKey("Teams", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username


class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100)
    project_description = models.CharField(max_length=1000)
    project_client = models.CharField(max_length=100)

    def __str__(self):
        return self.project_name


class Teams(models.Model):
    TEAM_LANGUAGE_CHOICES = [
        ("eng", "English"),
        ("fre", "French"),
        ("ger", "German"),
        ("ita", "Italian"),
        ("spa", "Spanish"),
    ]

    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100)
    team_description = models.CharField(max_length=1000)
    team_project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    team_team_lead = models.CharField(max_length=100)
    team_language = models.CharField(
        max_length=3, choices=TEAM_LANGUAGE_CHOICES, default="eng"
    )

    def __str__(self):
        return self.team_name

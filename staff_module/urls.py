from django.urls import path
from . import views

urlpatterns = [
    path("", views.manage_staff_classifier),
    path("admin/", views.manage_staff_admin),
    path("manager/", views.manage_staff_manager),
    path("team-leader/", views.manage_staff_team_leader),
]

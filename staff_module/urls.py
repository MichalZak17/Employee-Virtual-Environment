from django.urls import path
from . import views

urlpatterns = [
    path("manage-staff/", views.manage_staff_classifier),
    path("manage-staff/admin/", views.manage_staff_admin),
    path("manage-staff/manager/", views.manage_staff_manager),
    path("manage-staff/team-leader/", views.manage_staff_team_leader),
]

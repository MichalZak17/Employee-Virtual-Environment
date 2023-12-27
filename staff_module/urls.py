from django.urls import path
from . import views

urlpatterns = [
    path('manage-staff/', views.manage_staff, name='manage_staff'),  
]
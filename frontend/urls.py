from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.product, name='product'),
    path('use-cases/', views.use_cases, name='use_cases'),
    path('contact-us/', views.contact_us, name='contact_us'),

    path('admin/dashboard/', views.dashboard, name='dashboard'),    
]
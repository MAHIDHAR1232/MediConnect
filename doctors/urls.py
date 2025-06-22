from django.urls import path
from . import views
from .views import  profile, view_appointments,change_password

urlpatterns = [
  path('profile/', views.profile, name='doctor_profile'),
  path('change-password/', views.change_password, name='change_password'),
  path('doctor_view_appointments/', views.view_appointments, name='view_appointments'),
]


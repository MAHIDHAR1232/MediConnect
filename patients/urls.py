from django.urls import path
from . import views
from .views import  patient_dashboard, book_appointment, my_appointments ,patient_confirm_book
from doctors.views import profile
urlpatterns = [
  path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
  path('profile/', profile, name='patient_profile'),
  path('book_appointment/', views.book_appointment, name='book_appointment'),
  path('my_appointments/', views.my_appointments, name='my_appointments'),
  path('patient_confirm_book/<str:doctor>/', views.patient_confirm_book, name='patient_confirm_book'),

  
]
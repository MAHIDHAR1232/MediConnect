from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from datetime import datetime, date
from django.db.models import Q, Count
from django.urls import reverse
from django.core.files.storage import default_storage

from patients.models import Appointment, Status
from users.models import Doctors, Specialty

User = get_user_model()


@login_required(login_url='/login')
def profile(request):
    specialities = Specialty.objects.all()
    updated_profile_successfully = False

    if request.method == 'POST' and 'update_profile' in request.POST:
        user = request.user
        user.first_name = request.POST.get('user_firstname')
        user.gender = request.POST.get('user_gender')

        # Update doctor profile if the user is a doctor
        if user.is_doctor:
            specialty = request.POST.get('Speciality')
            try:
                specialty_name = Specialty.objects.get(name=specialty)
                doctor_profile = user.doctors
                doctor_profile.specialty = specialty_name
                doctor_profile.bio = request.POST.get('bio')
                doctor_profile.save()
            except Specialty.DoesNotExist:
                messages.error(request, 'Specialty not found. Please try again.')
                return redirect('update_profile')
        else:
            user.patients.save()

        if 'profile_pic' in request.FILES:
            user.profile_avatar = request.FILES['profile_pic']
        
        user.save()
        updated_profile_successfully = True

    return render(request, 'doctors/profile.html', context={
        "basicdata": request.user,
        "updated_profile_successfully": updated_profile_successfully,
        "specialities": specialities
    })


@login_required(login_url='/login')
def change_password(request):
    updated_password_successfully = False

    if request.method == 'POST' and 'update_password' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current Password is Incorrect. Please try again.')
        elif new_password != confirm_new_password:
            messages.error(request, 'New passwords do not match. Please try again.')
        elif len(new_password) < 6:
            messages.error(request, 'New password must be at least 6 characters long.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keeps the user logged in
            updated_password_successfully = True

    return render(request, 'doctors/passwordChange.html', context={
        "basicdata": request.user,
        "updated_password_successfully": updated_password_successfully
    })


@login_required(login_url='/login')
def view_appointments(request):
  if request.method == 'POST':
    status = request.POST.get("status")
    app_id = request.POST.get("app")

    app = Appointment.objects.get(id=app_id)
    status_id = Status.objects.get(status=status)
    app.status = status_id

    app.save()

  app = Appointment.objects.filter(doctor__user=request.user)

  filter_status = request.GET.get('filter_status')
  filter_date = request.GET.get('filter_date')
  filter_patient_name = request.GET.get('filter_patient_name')

  if filter_status and filter_status != 'All':
    app = app.filter(status__status=filter_status)

  if filter_date:
    app = app.filter(start_date=filter_date)

  if filter_patient_name:
    app = app.filter(patient__user__first_name__icontains=filter_patient_name)

  return render(request, "doctors/viewappointments.html", {
    'appointments': app,
    'filter_status': filter_status,
    'filter_date': filter_date,
    'filter_patient_name': filter_patient_name
  })


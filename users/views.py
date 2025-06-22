from django.shortcuts import render

from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import Patients , Reste_token
from .helpers import send_email
import uuid
from .models import Specialty, Doctors

Users = get_user_model()

def homeview(request):
  return render(request, 'users/base.html')

def serviceview(request):
  return render(request, 'users/service.html')

from django.core.paginator import Paginator

def DoctorListview(request):
    # Get all specialities and doctors
    specialities = Specialty.objects.all()
    doctors = Doctors.objects.all()
    
    # Fetch filter parameters from the GET request
    filter_speciality = request.GET.get('filter_speciality')
    filter_city = request.GET.get('filter_city')
    filter_doctor_name = request.GET.get('filter_doctor_name')

    # Apply filtering based on selected speciality
    if filter_speciality and filter_speciality != 'All':
        doctors = doctors.filter(specialty__name=filter_speciality)

    # Apply filtering based on doctor name (partial matching)
    if filter_doctor_name:
        doctors = doctors.filter(user__first_name__icontains=filter_doctor_name)

    # Paginate the doctors list (show 10 doctors per page)
    paginator = Paginator(doctors, 10)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    # Return rendered template with doctors and filters
    return render(request, "users/doctors.html", {
        'doctors': page_obj,  # Pass the paginated doctors
        'specialities': specialities,
        'filter_speciality': filter_speciality,
        'filter_doctor_name': filter_doctor_name,
        'filter_city': filter_city
    })




def register(request):
  if request.method == 'POST':
    user_status = 'Patient'  
    first_name = request.POST.get('user_firstname')
    profile_pic = ""

   # Check if profile picture is uploaded
    if "profile_pic" in request.FILES:
      profile_pic = request.FILES['profile_pic']
    else:
      # If no profile picture is uploaded, use a default image
      profile_pic = 'users/patient1.jpg'

    username = request.POST.get('user_id')
    email = request.POST.get('email')
    gender = request.POST.get('user_gender')
    password = request.POST.get('password')
    
    # Password length validation
    if len(password) < 6:
      messages.error(request, 'Password must be at least 6 characters long.')
      return render(request, 'users/register.html', context={'user_firstname': first_name, 'user_id': username, 'email': email, 'user_gender': gender})

    # Check if username already exists
    if Users.objects.filter(username=username).exists():
      messages.error(request, 'Username already exists. Try again with a different username.')
      return render(request, 'users/register.html', context={'user_firstname': first_name, 'user_id': username, 'email': email, 'user_gender': gender})

    # Check if Email already exists
    if Users.objects.filter(email=email).exists():
      messages.error(request, 'Email already exists. Try again with a different Email.')
      return render(request, 'users/register.html', context={'user_firstname': first_name, 'user_id': username, 'email': email, 'user_gender': gender})


    # Create the user (Patient)
    user = Users.objects.create_user(
      first_name=first_name,
      profile_avatar=profile_pic,
      username=username,
      email=email,
      gender=gender,
      password=password,
      is_doctor=False  # Always set to False
    )
    user.save()

    patient = Patients.objects.create(user=user) 
    patient.save()

    messages.success(request, 'Your account has been successfully registered. Please login.', extra_tags='success')

  # Returning the register page
  return render(request, 'users/register.html')



def login_view(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)

      if user.is_doctor:
        return redirect('homeview')

      elif Patients.objects.filter(user=user).exists():
        return redirect('homeview')
    else:
      messages.error(request, 'Incorrect username or password')
      
    return render(request, 'users/login.html')
  
  return render(request, 'users/login.html')



def forgot_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Users.objects.filter(email=email).first()  # Use `.first()` to avoid list

        if user:
            token = str(uuid.uuid4())

            # Check if a reset token already exists for this email
            reset, created = Reste_token.objects.get_or_create(user=user, email=user.email)
            
            if not created:
                # If token exists, update it instead of creating a new one
                reset.token = token  
                reset.save()
            else:
                reset.token = token  # Ensure token is saved even when newly created
                reset.save()

            sent = send_email(user.email, token)
            if sent:
                return render(request, 'users/forgot.html', context={'send_email_success': 1})

        else:
            return render(request, 'users/forgot.html', context={'errorlogin': 1})

    return render(request, 'users/forgot.html')



def forgot_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Users.objects.filter(email=email).first()
        if user:
            token = str(uuid.uuid4())
            reset = Reste_token.objects.create(
                user=user[0],
                email=user[0].email,  
                token=token  
            )
            reset.save()
            sent = send_email(user[0].email,token)
            if sent:
                return render(request, 'users/forgot.html',context={'send_email_succes': 1})
        else:
            return render(request, 'users/forgot.html', context={'errorlogin': 1})
    return render(request, 'users/forgot.html')





def reset_view(request,token):
    if request.method == 'POST':
        reste = Reste_token.objects.filter(token=token)
        print(reste)
        if reste:
            password = request.POST.get('password')
            confirm_password = request.POST.get('conf_password')
            if len(password) < 6:
                messages.error(request, 'Password must be at least 6 characters long.')
                return render(request, 'users/reset.html', {'token': token} )
            print(password)
            print(confirm_password)
            if password != confirm_password:
                messages.error(request, 'password do not match')
                return render(request, 'users/reset.html', {'token': token} )
            user = Users.objects.filter(email=reste[0].email).first()
            if user:
                hashed_password = make_password(password)
                user.password = hashed_password
                user.save()
                reste.delete()
                return redirect('login')
            else:
                return render(request, 'users/reset.html', {'token': token , 'errorlogin':1} )
        return render(request, 'users/reset.html', {'token': token} )
    return render(request, 'users/reset.html',{'token': token})




@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')

    return render(request, 'users/contact.html')

def about_us(request):
  return render(request, 'users/aboutUs.html')

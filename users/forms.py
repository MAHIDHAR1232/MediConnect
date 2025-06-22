from django import forms
from django.contrib.auth.hashers import make_password
from .models import Users, Doctors, Patients
    
from django import forms
from django.contrib.auth.hashers import make_password
from .models import Users, Patients

class DoctorCreationForm(forms.ModelForm):
    # Include necessary user fields
    username = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False)  
    gender = forms.ChoiceField(choices=Users.gender_choices, required=True)
    profile_avatar = forms.ImageField(required=False)

    class Meta:
        model = Doctors
        fields = ['specialty', 'bio']  

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk: 
            user = self.instance.user
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['gender'].initial = user.gender
            self.fields['profile_avatar'].initial = user.profile_avatar

    def save(self, commit=True):
        if self.instance.pk: 
            user = self.instance.user
        else:  
            user = Users()

        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.gender = self.cleaned_data['gender']
        user.is_doctor = True  

        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])


        if self.cleaned_data['profile_avatar']:
            user.profile_avatar = self.cleaned_data['profile_avatar']
        user.save()

        doctor = super().save(commit=False)
        doctor.user = user

        if commit:
            doctor.save()

        return doctor


class PatientCreationForm(forms.ModelForm):

    username = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False) 
    gender = forms.ChoiceField(choices=Users.gender_choices, required=True)
    profile_avatar = forms.ImageField(required=False)  

    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk: 
            user = self.instance.user
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['gender'].initial = user.gender
            if user.profile_avatar:
                self.fields['profile_avatar'].initial = user.profile_avatar  

    def save(self, commit=True):
        
        if self.instance.pk: 
            user = self.instance.user
        else:  
            user = Users()

        # Update user fields
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.gender = self.cleaned_data['gender']
        user.is_doctor = False  
        user.is_active = True

        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])


        if self.cleaned_data['profile_avatar']:
            user.profile_avatar = self.cleaned_data['profile_avatar']

        user.save()

        patient = super().save(commit=False)
        patient.user = user

        if commit:
            patient.save()

        return patient


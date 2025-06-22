from django.contrib import admin
from .models import Users, Doctors, Specialty, Patients
from .forms import DoctorCreationForm


class DoctorsAdmin(admin.ModelAdmin):
    form = DoctorCreationForm  
    list_display = ['get_username', 'get_full_name', 'get_email', 'specialty', 'bio']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'specialty__name']

    fieldsets = (
        ('User Information', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'password', 'gender', 'profile_avatar')
        }),
        ('Doctor Details', {
            'fields': ('specialty', 'bio')
        }),
    )

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

admin.site.register(Doctors, DoctorsAdmin)
admin.site.register(Specialty)



from django.contrib import admin
from django.utils.html import format_html
from .models import Patients
from .forms import PatientCreationForm

class PatientAdmin(admin.ModelAdmin):
    form = PatientCreationForm  
    list_display = ['get_username', 'get_full_name', 'get_email']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']

    fieldsets = (
        ('User Information', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'password', 'gender', 'profile_avatar')
        }),
    )

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

   

admin.site.register(Patients, PatientAdmin)

from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')



class UsersAdmin(admin.ModelAdmin):
    list_display = ('username',)  


admin.site.register(Users, UsersAdmin)
    





































    
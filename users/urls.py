from django.urls import path
from .views import register, login_view, forgot_view, reset_view,logout_view, homeview, serviceview, DoctorListview,contact_us,about_us
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', homeview, name='homeview'),
    path('service/', serviceview, name='serviceview'),
    path('DoctorListview/', DoctorListview , name='DoctorListview'),
    path('contact/', contact_us, name='contact'),
    path('about-us/', about_us, name='about_us'),




    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('password-reset/', forgot_view, name='password-reset'),
    path('reset/<str:token>/', reset_view, name='reset'),
    path('logout/', logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=staticfiles_urlpatterns()

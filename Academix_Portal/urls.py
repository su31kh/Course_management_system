from django.contrib import admin
from django.urls import path, include
from Academix_Portal import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('land', views.landing, name="LandingPage"),
    path('studentlogin', views.studentlogin, name="studlogin"),
    path('adminlogin', views.adminlogin, name="adminlogin"),
    path('register', views.register, name="Register"),
    path('ver_reg', views.reg_validate, name="Reg_Validate"),
    

]

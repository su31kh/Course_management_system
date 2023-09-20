from django.contrib import admin
from django.urls import path, include
from Academix_Portal import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.home, name="HomePage"),
    path('studentlogin', views.studentlogin, name="studlogin"),
    path('adminlogin', views.adminlogin, name="adminlogin"),
    path('register', views.register, name="Register"),
    path('ver_reg', views.reg_validate, name="Reg_Validate"),
    path('addcourses' , views.addcourse , name = "Add_course"),
    path('enroll/<str:course_id>' , views.add_course_to_user , name="enroll")
]

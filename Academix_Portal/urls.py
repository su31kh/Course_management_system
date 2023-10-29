from django.contrib import admin
from django.urls import path, include
from Academix_Portal import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.home, name="HomePage"),
    path('login/<str:loginid>', views.login_func, name="login_func"),
    path('register', views.register, name="Register"),
    path('admindashboard', views.admindashboard, name="admindashboard"),
    path('coursedashboard', views.coursedashboard, name="coursedashboard"),
    path('announcements', views.announcements, name="announcements"),
    path('addannouncement', views.addannouncement, name="addannouncement"),
    path('materials', views.materials, name="materials"),
    path('assignments', views.assignments, name="assignments"),
    path('feedback', views.feedback, name="feedback"),
    path('actions', views.actions, name="actions"),
    path('otp_ver', views.reg_validate, name="otp_ver"),
    path('addcourses' , views.addcourse , name = "Add_course"),
    path('enroll/<str:course_id>' , views.add_course_to_user , name="enroll"),
    path('enroll/<str:course_id>' , views.add_course_to_user , name="enroll"),
    path('createassignment', views.createassignment, name="createassignment"),
    path('createsubmission', views.createsubmission, name="createsubmission"),
    path('mycourses/<str:course_id>/addassignment' , views.add_assignment , name="add_assignment"),
    path('mycourses/<str:course_id>/<str:name>/add_submission', views.add_submission, name="add_submission"),
    path('coursedashboard', views.coursedashboard, name="coursedashboard"),
    path('mycourse' , views.mycourse , name = "mycourse")
]

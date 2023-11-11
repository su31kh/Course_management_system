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

    path('mycourse', views.mycourse, name="mycourse"),
    path('mycourse/<str:course_id>/editcourse', views.edit_course, name="edit_course"),

    path('student_profile', views.students_profile, name="students_profile"),

    path('mycourse/<str:course_id>', views.announcements, name="announcements"),
    path('mycourse/<str:course_id>/addannouncement', views.addannouncement, name="addannouncement"),

    path('mycourse/<str:course_id>/createassignment', views.createassignment, name="createassignment"),
    path('mycourse/<str:course_id>/addassignment', views.add_assignment, name="add_assignment"),
    path('mycourse/<str:course_id>/viewassignments', views.view_assignments, name="view_assignments"),
    path('mycourse/<str:course_id>/<str:name>/editassignment', views.edit_assignment, name="edit_assignment"),


    path('mycourses/<str:course_id>/<str:name>/addsubmission', views.add_submission, name="add_submission"),
    path('mycourses/<str:course_id>/<str:name>/editsubmission', views.edit_submission, name="edit_submission"),
    path('mycourse/<str:course_id>/<str:name>/viewstudentssubmission', views.view_students_submission, name="view_students_submission"),

    path('mycourse/<str:course_id>/materials', views.materials, name="materials"),
    path('mycourse/<str:course_id>/addmaterial', views.addmaterial, name="addmaterial"),
    
    path('mycourse/<str:course_id>/feedback', views.fb_response, name="feedback"),
    path('coursedashboard',views.coursedashboard,name="coursedashboard"),
    path('actions', views.actions, name="actions"),
    path('actions_student', views.actions_student, name="actions_student"),
    path('otp_ver', views.verifyRegistration, name="otp_ver"),
    path('addcourses' , views.addcourse , name = "Add_course"),
    path('enroll/<str:course_id>' , views.add_course_to_user , name="enroll"),

    path('mycourse/<str:course_id>/studentlist',views.student_list , name= "student_list"),
    path('mycourse/<str:course_id>/studentlist/search',views.student_list_search , name= "student_list_search"),
    path('mycourse/<str:course_id>/studentlist/<str:id>/viewprofile',views.view_profile , name= "view_profile"),
    path('<str:course_id>/<str:student>',views.students_assignment , name= "students_assignment"),

    path('logout',views.log_out,name='log_out')
]

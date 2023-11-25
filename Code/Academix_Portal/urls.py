from django.contrib import admin
from django.urls import path, include
from Academix_Portal import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('error',views.error, name="error"),
    path('', views.home, name="HomePage"),
    path('login/<str:loginid>', views.login_func, name="login_func"),
    path('register', views.register, name="Register"),

    path('mycourse', views.mycourse, name="mycourse"),
    path('mycourse/search', views.mycourse_search, name="mycourse_search"),
    path('mycourse/<str:course_id>/editcourse', views.edit_course, name="edit_course"),
    path('mycourse/<str:course_id>/unenrollcourse', views.unenroll, name="unenroll"),
    path('mycourse/<str:course_id>/deletecourse', views.deletecourse, name="deletecourse"),
    
    
    path('student_profile', views.students_profile, name="students_profile"),

    path('mycourse/<str:course_id>', views.announcements, name="announcements"),
    path('mycourse/<str:course_id>/addannouncement', views.addannouncement, name="addannouncement"),
    path('mycourse/<str:course_id>/deleteannouncement/<str:ann_id>', views.delete_announcement, name="delete_announcement"),

    path('mycourse/<str:course_id>/createassignment', views.createassignment, name="createassignment"),
    path('mycourse/<str:course_id>/addassignment', views.add_assignment, name="add_assignment"),
    path('mycourse/<str:course_id>/viewassignments', views.view_assignments, name="view_assignments"),
    path('mycourse/<str:course_id>/<str:name>/editassignment', views.edit_assignment, name="edit_assignment"),
    path('mycourse/<str:course_id>/<str:name>/deleteassignment', views.delete_assignment, name="delete_assignment"),
    

    path('mycourses/<str:course_id>/<str:name>/addsubmission', views.add_submission, name="add_submission"),
    path('mycourses/<str:course_id>/<str:name>/editsubmission', views.edit_submission, name="edit_submission"),
    path('mycourse/<str:course_id>/<str:name>/viewstudentssubmission', views.view_students_submission, name="view_students_submission"),
    path('mycourse/<str:course_id>/<str:name>/viewstudentssubmission/<str:sub_id>/grade', views.grade_student_submission, name="grade_student_submission"),

    path('mycourse/<str:course_id>/materials', views.materials, name="materials"),
    path('mycourse/<str:course_id>/addmaterial', views.addmaterial, name="addmaterial"),

    path('mycourse/<str:course_id>/viewquery', views.view_query, name="view_query"),
    path('mycourse/<str:course_id>/addquery', views.add_query, name="add_query"),
    path('mycourse/<str:course_id>/replyquery/<str:qid>', views.reply_query, name="reply_query"),
    
    path('mycourse/<str:course_id>/feedback', views.fb_response, name="feedback"),
    path('coursedashboard',views.coursedashboard,name="coursedashboard"),
    path('coursedashboard/search',views.coursedashboard_search,name="coursedashboard_search"),
    path('otp_ver', views.verifyRegistration, name="otp_ver"),
    path('addcourses' , views.addcourse , name = "Add_course"),
    path('enroll/<str:course_id>' , views.add_course_to_user , name="enroll"),

    path('mycourse/<str:course_id>/studentlist',views.student_list , name= "student_list"),
    path('mycourse/<str:course_id>/studentlist/search',views.student_list_search , name= "student_list_search"),
    path('mycourse/<str:course_id>/studentlist/<str:id>/viewprofile',views.view_profile , name= "view_profile"),
    path('student_profile/change',views.update_profile, name="update_profile"),
    path('<str:course_id>/<str:student>',views.students_assignment , name= "students_assignment"),
    path('logout/',views.log_out,name='log_out'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name="password_reset_complete"),
]

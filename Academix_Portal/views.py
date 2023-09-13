from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader


def landing(request):
    t = loader.get_template("land.html")
    return render(request , 'land.html')

def studentlogin(request):
    student_login = loader.get_template("login_page_student.html")
    return render(request , 'login_page_student.html')

def adminlogin(request):
    student_login = loader.get_template("login_page_admin.html")
    return render(request , 'login_page_admin.html')
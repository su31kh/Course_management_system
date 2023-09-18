from django.shortcuts import render
import requests

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
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

# def reg_validate(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         code=1234
#         return register(request, email, code)
#     return render(request, 'Verification_Reg.html')


def register(request, email, code):

    if request.method == "GET":
        return render(request, 'register.html')

    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        batch = request.POST['batch']
        branch = request.POST['branch']
        program = request.POST['program']
        ver_code = request.POST['ver_code']
        if code == ver_code:
            user = User.objects.create_user(username=username, email=email, password=password)
            my_profile = Profile.objects.create(user=request.user, first_name=first_name, middle_name=middle_name, last_name=last_name, batch=batch, branch=branch, program=program)
            my_profile.save()
        else:
            return render(request,'register.html')
        return render(request,'land.html')
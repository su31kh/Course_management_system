from django.shortcuts import render, redirect
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

def reg_validate(request):
    if request.method == "POST":
        email = request.POST['email']
        code=1234
        request.session['code'] = code
        request.session['email'] = email
        return redirect('/register')
    return render(request, 'Verification_Reg.html')


def register(request):

    if request.method == "GET":
        return render(request, 'register.html')

    if request.method == "POST":
        email = request.session.get('email', None)
        code = request.session.get('code', None)
        # print(email)
        # print(code)
        code = str(code)
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        batch = request.POST.get('batch')
        branch = request.POST.get('branch')
        program = request.POST.get('program')
        ver_code = request.POST.get('ver_code')
        # print(type(ver_code))
        if code == ver_code:
            user = User.objects.create_user(username=username, email=email, password=password)
            my_profile = Profile.objects.create(user=username, first_name=first_name, middle_name=middle_name, last_name=last_name, batch=batch, branch=branch, program=program)
            my_profile.save()
        else:
            return render(request,'register.html')
        return render(request,'land.html')
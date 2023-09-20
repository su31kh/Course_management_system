from django.shortcuts import render, redirect
import requests
import random
from .utils import send_email_to_client
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import student_profile
from django.template import loader
from django.contrib.auth import authenticate


def home(request):
    return render(request , 'land.html')

def studentlogin(request):
    if request.method == "POST":
        username = request.POST['user']
        passwrd = request.POST['pass']
        user = authenticate(username=username, password=passwrd)
        if user is not None:
            context = {'user':user}
            return render(request, 'check.html', context)
        else:
            return redirect('/studentlogin')
    else:
        return render(request , 'login_page_student.html')

def adminlogin(request):
    #student_login = loader.get_template("login_page_admin.html")
    return render(request , 'login_page_admin.html')

def reg_validate(request):
    if request.method == "POST":
        email = request.POST['email']
        code = random.randint(1000,9999)
        request.session['code'] = code
        request.session['email'] = email
        send_email_to_client(email, code)
        return redirect('/register')
    return render(request, 'Verification_Reg.html')


def register(request):

    if request.method == "GET":
        return render(request, 'register.html')

    if request.method == "POST":
        email = request.session.get('email', None)
        code = request.session.get('code', None)
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
        if code == ver_code:
            user = User.objects.create_user(username=username, email=email, password=password)
            my_profile = student_profile.objects.create(user=user, first_name=first_name, middle_name=middle_name, last_name=last_name, batch=batch, branch=branch, program=program)
            my_profile.save()
        else:
            return render(request,'register.html')
        return render(request,'land.html')
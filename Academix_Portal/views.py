from django.shortcuts import render, redirect
import requests
import random
from .utils import send_email_to_client
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import student_profile
from .models import faculty_profile
from .models import Course
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login

from django.contrib import messages

def home(request):
    return render(request , 'land.html')

def login(request, loginid):
    if request.method == "POST":
        username = request.POST['user']
        passwrd = request.POST['pass']
        user = authenticate(username=username, password=passwrd)
        if user is None:
            messages.warning(request, "Please Enter the correct Credentials.")
            return redirect('/studentlogin')
        if loginid == "faculty":
            context = {'user':user}
            return render(request, 'home.html', context)
        elif loginid == "student":
            context = {'user':user}
            return render(request, 'home.html', context)
    else:
        if loginid == "student":
            return render(request , 'login_page_student.html')
        else:
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
        password = request.POST.get('pass1')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        batch = request.POST.get('batch')
        branch = request.POST.get('branch')
        program = request.POST.get('program')
        ver_code = request.POST.get('ver_code')

        if User.objects.filter(email=email).first is not None:
            messages.warning(request, "Enter correct Email")
            return redirect('/register')
        if User.objects.filter(username=username).first is not None:
            messages.warning(request, "Enter correct Email")
            return redirect('/register')

        if code == ver_code:
            user = User.objects.create_user(username=username, email=email, password=password)
            my_profile = student_profile.objects.create(user=user, first_name=first_name, middle_name=middle_name, last_name=last_name, batch=batch, branch=branch, program=program)
            my_profile.save()
            user = authenticate(request, username=username, password=password)
            login(request,user)
        else:
            return render(request,'register.html')
        return render(request,'home.html')


def addcourse(request):

    if(request.method == 'POST'):
        course_name = request.POST.get('coursename')
        courseid = request.POST.get('courseid')
        description = request.POST.get('description')
        faculty = request.POST.get('faculty')
        my_course = Course.objects.create(name = course_name , course_code = courseid , description = description , faculty = faculty)

        my_course.save()

    return render(request , 'addcourse.html')



def add_course_to_user(request, course_id):
    try:
        current_user = request.user
        course = get_object_or_404(Course, course_code=course_id)

        if course.studentlist.filter(user = current_user).exists():
            return JsonResponse({'error': 'User is already enrolled in this course'}, status=400)

        course.studentlist.add(current_user)
        current_user.student_courses.add(course)

        course.save()
        current_user.save()

        return JsonResponse({'message': 'User successfully enrolled in the course'})

    except Exception as e:
        
        return JsonResponse({'error': str(e)}, status=500)
        

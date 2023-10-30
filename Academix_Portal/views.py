from django.shortcuts import render, redirect
import requests
import random
from .utils import send_email_to_client
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import student_profile
from .models import faculty_profile
from .models import Course, Assignment, Submission, Announcements
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib import messages

def home(request):
    return render(request , 'land.html')

def admindashboard(request):
    return render(request , 'admin_dashboard.html')

def coursedashboard(request):
    return render(request , 'course_dashboard_student.html')

def actions(request):
    return render(request , 'actions.html')

def announcements(request):
    return render(request , 'announcements.html')

def assignments(request):
    return render(request , 'assignments.html')

def materials(request):
    return render(request , 'materials.html')

def addannouncement(request):
    return render(request , 'add_announcement.html')

def feedback(request):
    return render(request , 'feedback.html')

def login_func(request, loginid):
    if request.method == "POST":
        username = request.POST.get('user')
        passwrd = request.POST.get('pass')
        user = authenticate(request , username=username, password=passwrd)
        if user is None:
            messages.warning(request, "Please Enter the correct Credentials.")
            print("1")
            return redirect('/login/student')
        if loginid == "faculty":
            context = {'user':user}
            login(request, user)
            print("2")
            return render(request, 'home.html', context)
            # return redirect('/')
        elif loginid == "student":
            context = {'user':user}
            print(user)
            login(request, user)
            print("3")
            # return redirect('/')
            return render(request, 'home.html', context)
    else:
        print("4")
        if loginid == "student":
            return render(request , 'login_page_student.html')
        else:
            return render(request , 'login_page_admin.html')
        

def register(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST.get('pass1')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        batch = request.POST.get('batch')
        branch = request.POST.get('branch')
        program = request.POST.get('program')
        code = random.randint(1000,9999)
        request.session['code'] = code
        send_email_to_client(email, code)
        dict = {'email':email,'password':password,'first_name':first_name,'middle_name':middle_name,'last_name':last_name,'batch':batch,'branch':branch,'program':program }
        return render(request,'otp_ver.html',dict)
    else:
        return redirect('/')

def verifyRegistration(request):
    if request.method == "POST":
        code = request.session.get('code', None)
        email = request.POST['email']
        password = request.POST.get('pass1')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        batch = request.POST.get('batch')
        branch = request.POST.get('branch')
        program = request.POST.get('program')
        code = str(code)
        ver_code = request.POST.get('ver_code')
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Enter correct Email")
            return redirect('/register')
        if code == ver_code:
            user = User.objects.create_user(username=email, email=email, password=password)
            my_profile = student_profile.objects.create(user=user, first_name=first_name, middle_name=middle_name, last_name=last_name, batch=batch, branch=branch, program=program)
            my_profile.save()
            user = authenticate(request, username=email, password=password)
            login(request,user)
            return render(request,'home.html')
        else:
            messages.error("PLEASE ENTER CORRECT OTP")
            return render(request,'register.html')
    else:
        return redirect('/')

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
        print(current_user)
        course = Course.objects.get(course_code = course_id)
        print(course)
        if course.studentlist.filter(user = current_user).exists():
            return JsonResponse({'error': 'User is already enrolled in this course'}, status=400)
        studentuser = student_profile.objects.get(user = current_user)
        course.studentlist.add(studentuser)
        studentuser.student_courses.add(course)

        course.save()
        studentuser.save()

        return JsonResponse({'message': 'User successfully enrolled in the course'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def coursedashboard(request):
    course = Course.objects.all()
    context = {
        "courses":course,
    }
    return render(request , 'course_dashboard_student.html' , context)

def mycourse(request):
    current_user = request.user
    student = student_profile.objects.get(user = current_user)
    print(student)
    myenroll = student.student_courses.all()
    print((myenroll))
    
    context = {
        'enrolled': myenroll,
    }
    return render(request , 'enrolledcourse.html' , context)

def createassignment(request):
    return render(request, 'add_assignment.html')  

def add_assignment(request, course_id):
    print(course_id)
    course = Course.objects.get(course_code = course_id)
    print(course)
    if(request.method == 'POST'):
        assignmentname = request.POST.get('assignmentname')
        description = request.POST.get('description')
        duedate = request.POST.get('duedate')
        max_grade = request.POST.get('max_grade')
        attachment = request.POST.get('attachment')
        assignment = Assignment.objects.create(name = assignmentname, description = description, duedate = duedate, max_grade=max_grade, attachment = attachment, assignment_course = course)

        assignment.save()

    return render(request, 'add_assignment.html')

def createsubmission(request):
    return render(request, 'add_submission.html')

def add_submission(request, course_id, name):
    student = student_profile.objects.get(user = request.user)
    assignment = Assignment.objects.get(name = name)
    if(request.method == 'POST'):
        work = request.POST.get('work')
        submission = Submission.objects.create(student = student, assignment = assignment, work = work)
        submission.save()

    if(submission.timestamp <= assignment.duedate):
        submission.feedback='Turned in'
    else:
        submission.feedback='Turned in late'
    submission.save()
    return render(request, 'add_submission.html')

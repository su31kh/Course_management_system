from django.shortcuts import render, redirect, HttpResponseRedirect
import requests
import random
from .utils import send_email_to_client
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import student_profile
from .models import faculty_profile
from .models import Course, Assignment, Submission, Announcements, Material
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

def home(request):
    return render(request , 'land.html')

def admindashboard(request):
    return render(request , 'admin_dashboard.html')

def students_profile(request):
    return render(request , 'student_profile.html')

def actions_student(request):
    return render(request , 'actions_student.html')

def actions(request):
    return render(request , 'actions.html')

def materials(request,course_id):
    course = Course.objects.get(course_code=course_id)
    material = Material.objects.filter(course=course)
    context = {
        'material':material,
        'course':course
    }
    return render(request , 'materials.html', context)

def addmaterial(request,course_id):
    if request.method == "POST":
        course = Course.objects.get(course_code=course_id)
        title = request.POST.get('title')
        desc = request.POST.get('description')
        file = request.POST.get('file')
        material_files = Material.objects.create(title=title,description=desc, course=course, material_file=file)
        material_files.save()
        return redirect('/mycourse/'+course_id+"/materials")
    else:
        course = Course.objects.get(course_code=course_id)
        context = {
            'course':course
        }
        return render(request , 'add_material.html', context)

def announcements(request , course_id):
    course = Course.objects.get(course_code=course_id)
    announce = Announcements.objects.filter(course=course)
    context = {
        "course":course,
        "announce":announce
    }
    return render(request , 'announcements.html', context)

def addannouncement(request,course_id):
    user = request.user
    prof = faculty_profile.objects.filter(user=user)
    # print(prof)
    if not prof:
        messages.error(request,"You cannot post an announcement")
        return redirect('/mycourse/'+course_id)
    else:
        if request.method == "POST":
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            course = Course.objects.get(course_code=course_id)
            my_announce = Announcements.objects.create(title=title, description=desc, course=course, user=request.user)
            my_announce.save()
            return redirect('/mycourse/'+course_id)
        else:
            course = Course.objects.get(course_code=course_id)
            context = {
                "course":course
            }
            return render(request , 'add_announcement.html', context)

def feedback(request):
    return render(request , 'feedback.html')

def login_func(request, loginid):
    if request.method == "POST":
        username = request.POST.get('user')
        passwrd = request.POST.get('pass')
        user = authenticate(request , username=username, password=passwrd)
        if user is None:
            messages.warning(request, "Please Enter the correct Credentials.")
            # print("1")
            return redirect('/login/student')
        if loginid == "faculty":
            context = {'user':user}
            login(request, user)
            print("2")
            # return render(request, 'home.html', context)
            return redirect('/')
        elif loginid == "student":
            context = {'user':user}
            print(user)
            login(request, user)
            # print("3")
            return redirect('/mycourse')
            # return render(request, 'home.html', context)
    else:
        # print("4")
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

def edit_course(request, courseid):
    if(request.method == 'POST'):
        editcourse = Course.objects.get(course_code = courseid)
        editcourse.name = request.POST.get('coursename')
        editcourse.course_code = request.POST.get('courseid')
        editcourse.description = request.POST.get('description')
        editcourse.faculty = request.POST.get('faculty')
        editcourse.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def student_list(request , course_id):
    current_course = Course.objects.get(course_code = course_id)
    students = current_course.studentlist.all()

    context = {
        "students":students,
        "course_id":course_id
    }

    return render(request , 'student_list.html' , context)

def students_assignment(request , course_id , student):

    course = Course.objects.get(course_code=course_id)
    assign = Assignment.objects.filter(assignment_course=course).all()

    thisstudent = student_profile.objects.get(first_name = student)
    print(thisstudent)
    
    submitlist = []
    for a in assign :
        if(Submission.objects.filter(assignment = a , student = thisstudent).exists()):
            submitlist.append(Submission.objects.get(assignment = a , student = thisstudent))

    context = {
        "submission":submitlist
    }
    return render(request , 'students_assignment.html' , context)

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
    current_user = request.user
    student = student_profile.objects.get(user = current_user)
    myenroll = student.student_courses.all()

    final = course.difference(myenroll)
    context = {
        "courses":final,
    }
    return render(request , 'course_dashboard_student.html' , context)

def mycourse(request):
    current_user = request.user
    student = student_profile.objects.get(user = current_user)
    # print(student)
    myenroll = student.student_courses.all()
    # print((myenroll))
    
    context = {
        'enrolled': myenroll,
    }
    return render(request , 'my_course_student.html' , context)

def createassignment(request, course_id):
    params = {
        "courseid":course_id
    }
    return render(request, 'add_assignment.html', params)

def add_assignment(request, course_id):
    user = request.user
    prof = faculty_profile.objects.filter(user=user)
    if prof is None:
        messages.error(request,"You cannot post an announcement")
    else:
        course = Course.objects.get(course_code = course_id)
        if(request.method == 'POST'):
            assignmentname = request.POST.get('name')
            description = request.POST.get('description')
            duedate = request.POST.get('duedate')
            max_grade = request.POST.get('max_grade')
            attachment = request.POST.get('attachment')
            assignment = Assignment.objects.create(name = assignmentname, description = description, duedate = duedate, max_grade=max_grade, attachment = attachment, assignment_course = course)

            assignment.save()

    return redirect('/mycourse/'+course_id+'/viewassignments')

def view_assignments(request,course_id):
    course = Course.objects.get(course_code=course_id)
    assign = Assignment.objects.filter(assignment_course=course)
    student_prof = student_profile.objects.get(user=request.user)
    submit=[]
    for x in assign:
        y = Submission.objects.filter(student=student_prof).filter(assignment=x)
        submit.append(y)
    merged = tuple(zip(assign, submit))
    param = {
        'course':course,
        'merged':merged
    }
    return render(request , 'view_assignments.html', param)

def edit_assignment(request, course_id):
    if request.method == 'POST':
        editassignment = Assignment.objects.get()
        editassignment.name = request.POST.get('name')
        editassignment.description = request.POST.get('description')
        editassignment.duedate = request.POST.get('duedate')
        editassignment.max_grade = request.POST.get('max_grade')
        editassignment.attachment = request.POST.get('attachment')
        editassignment.save()

    return redirect('/mycourse/'+course_id+'/viewassignments')
        


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


    return redirect('/mycourse/'+course_id+'/viewassignments')

def edit_submission(request, course_id, name):
    if(request.method == 'POST'):
        editsubmission = Submission.objects.get()
        editsubmission.work = request.POST.get('work')
        editsubmission.save()

    return redirect('/mycourse/'+course_id+'/viewassignments')

def log_out(request):
    logout(request)
    return redirect('/')



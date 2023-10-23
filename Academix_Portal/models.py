from django.db import models
from django.contrib.auth.models import User

from django.contrib.postgres.fields import ArrayField


class student_profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=False)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, null=False)
    batch = models.IntegerField(null=False)
    branch = models.CharField(max_length=50, null=False)
    program = models.CharField(max_length=50, null=False)
    student_courses = models.ManyToManyField('Course', related_name='studentslist', blank=True)

    def __str__(self):
        return self.user.username


class faculty_profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) 
    name = models.CharField(max_length=30, null=False , default = "Name")

    faculty_courses = models.ManyToManyField('Course', related_name='facultylist', blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=25, unique=True)
    course_code = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True, null=True)
    faculty = models.CharField(max_length=25, unique=False)
    studentlist = models.ManyToManyField('student_profile', related_name='course', blank=True)

    def __str__(self):
        return self.name
class Assignment(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    duedate = models.DateTimeField()
    max_grade = models.IntegerField()
    attachment = models.URLField()
    assignment_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class Submission(models.Model):
    student = models.ForeignKey(student_profile, on_delete=models.CASCADE)
    graded = models.BooleanField(default=False)
    grade = models.IntegerField(null=True)
    work = models.URLField()
    feedback = models.CharField(max_length=20, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    def __str__(self):
        return self.assignment.assignment_course.course_code + ' ' + self.student.first_name + self.student.last_name
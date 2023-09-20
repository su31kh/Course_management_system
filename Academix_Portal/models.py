from django.db import models
from django.contrib.auth.models import User

from django.contrib.postgres.fields import ArrayField


class student_profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=False)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, null=False)
    batch = models.IntegerField(null=False)
    branch = models.CharField(max_length=50, null=False)
    program = models.CharField(max_length=50, null=False)
    student_courses = models.ManyToManyField('Course', related_name='studentslist', blank=True)


class faculty_profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
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


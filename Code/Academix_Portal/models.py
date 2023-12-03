from django.db import models
from django.contrib.auth.models import User

from django.contrib.postgres.fields import ArrayField


class student_profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=False)
    middle_name = models.CharField(max_length=20, null = True, blank= True)
    last_name = models.CharField(max_length=20, null=False)
    batch = models.IntegerField(null=False)
    branch = models.CharField(max_length=50, null=False)
    program = models.CharField(max_length=50, null=False)
    student_courses = models.ManyToManyField('Course', related_name='studentslist', blank=True)

    def __str__(self):
        return self.user.username


class faculty_profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=False, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=20, null=False)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=False)
    faculty_courses = models.ManyToManyField('Course', related_name='facultylist', blank=True)

    def __str__(self):
        return self.first_name

class Course(models.Model):
    name = models.CharField(max_length=25, unique=True)
    course_code = models.CharField(max_length=25, unique=True)
    description = models.TextField(max_length=30, blank=True, null=True)
    faculty = models.ForeignKey(faculty_profile, on_delete=models.CASCADE)
    studentlist = models.ManyToManyField('student_profile', related_name='course', blank=True)

    def __str__(self):
        return self.name
    
class Assignment(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100, null=True, blank=True)
    duedate = models.DateTimeField()
    max_grade = models.IntegerField()
    attachment =models.FileField(upload_to='attachments')
    assignment_course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('name' , 'assignment_course')
    
class Submission(models.Model):
    student = models.ForeignKey(student_profile, on_delete=models.CASCADE)
    graded = models.BooleanField(default=False)
    grade = models.IntegerField(null=True)
    work = models.FileField(upload_to='submissions')
    feedback = models.CharField(max_length=20, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    def __str__(self):
        return self.assignment.assignment_course.course_code + ' ' + self.student.first_name + self.student.last_name
    
    class Meta:
        unique_together = ('student', 'assignment')
    
class Announcements(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=100, null=True)
    material_file = models.FileField(upload_to='materials')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course.course_code + ' ' + self.title
    

class feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    fb = models.CharField(max_length=200,null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.course_code + ' ' + self.user.email
    
class query(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(student_profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    qry = models.CharField(max_length=200,null=False)
    reply = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.course.course_code + ' ' + self.user.first_name + ' ' + self.user.last_name
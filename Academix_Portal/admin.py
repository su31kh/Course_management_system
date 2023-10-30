from django.contrib import admin
from .models import student_profile
from .models import faculty_profile
from .models import Course, Assignment, Submission, Announcements

admin.site.register(student_profile)
admin.site.register(faculty_profile)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Announcements)
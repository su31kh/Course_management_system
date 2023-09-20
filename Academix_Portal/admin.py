from django.contrib import admin
from .models import student_profile
from .models import faculty_profile


admin.site.register(student_profile)
admin.site.register(faculty_profile)
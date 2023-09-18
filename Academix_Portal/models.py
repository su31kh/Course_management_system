from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=False)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, null=False)
    batch = models.IntegerField(null=False)
    branch = models.CharField(max_length=50, null=False)
    program = models.CharField(max_length=50, null=False)
    gender = models.CharField(max_length=1, null=False)

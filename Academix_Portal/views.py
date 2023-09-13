from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader


def landing(request):
    t = loader.get_template("login_page_admin.html")
    return render(request , 'login_page_admin.html')
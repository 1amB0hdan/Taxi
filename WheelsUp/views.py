from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home (request):
    return render(request, 'home/home.html')

def login_view(request):
    return render(request, 'login/login.html')
def register_view(request):
    return render(request, 'register/register.html')

def profile_view(request):
    return render(request, 'profile/profile.html')
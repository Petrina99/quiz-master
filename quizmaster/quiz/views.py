from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.
def home(request):

    context = {}
    return render(request, 'quiz/home.html', context)

def register_user(request):

    context = {}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        repeat_password = request.POST['repeat-password']

        does_exist = User.objects.filter(username=username).exists()

        if does_exist is False:
            if password == repeat_password:
                user = User.objects.create_user(username = username, password = password)
               
                user.save()
                # odma nakon registracije logiramo korisnika
                new_user = authenticate(username=username, password=password)
                login(request, new_user)
                return HttpResponseRedirect('/')
            else:
                context = {
                    'error': "Passwords don't match"
                }
                return render(request, 'registration/register.html', context)
        else:
            context = {
                'error': "User with that username already exists"
            }
            return render(request, 'registration/register.html', context)
            
    return render(request, 'registration/register.html')

def login_user(request):

    context = {}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            context = {
                'error': "Invalid credentials"
            }
        
            return render(request, 'registration/login.html', context)
    
    return render(request, 'registration/login.html')
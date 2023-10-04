from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def auth_login(request):
    if request.method == 'POST':
        team = request.POST['team']
        password = request.POST['password']
        user = authenticate(request,username=team,password=password)
        if user:
            login(request,user)
            if user.is_superuser:
                return redirect('admin_home')
            else:
                return redirect('home')

    return render(request,'login.html')


def auth_register(request):
    if request.method == 'POST':
        team=request.POST['team']
        manager=request.POST['manager']
        coach=request.POST['coach']
        password=request.POST['password']
        if CustomUser.objects.filter(username=team).exists():
            messages.info(request,'Team name is taken')
            return redirect('register')
        else:
            user = CustomUser.objects.create_user(
                username=team,manager=manager,coach=coach,password=password
            )
            return redirect('login')
    return render(request,'register.html')


def auth_logout(request):
    logout(request)
    return redirect('home')
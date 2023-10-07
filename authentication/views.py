from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

# Login View
def auth_login(request):
    if request.method == 'POST':
        team = request.POST['team']
        password = request.POST['password']
        user = authenticate(request,username=team,password=password)
        if user:
            login(request,user)
            if user.is_superuser:
                # Redirect to admin home if the user is an admin
                return redirect('admin_home')
            else:
                # Redirect to Users home
                return redirect('home')

    return render(request,'login.html')

# Register View
def auth_register(request):
    total_users = CustomUser.objects.count()
    print('total_users:',total_users)
    if total_users > 10:
        # If there are already 10 or more users, redirect to login
        return redirect('login')
    else:
        if request.method == 'POST':
            team=request.POST['team']
            manager=request.POST['manager']
            coach=request.POST['coach']
            password=request.POST['password']
            if CustomUser.objects.filter(username=team).exists():
                # Display an error message if the team name is already taken
                messages.info(request,'Team name is taken')
                return redirect('register')
            else:
                # Create a new Team
                user = CustomUser.objects.create_user(
                    username=team,manager=manager,coach=coach,password=password
                )
                return redirect('login')
        return render(request,'register.html')

# Logout View
def auth_logout(request):
    logout(request)
    # Log the user out and redirect to login page
    return redirect('login')

# Check Signup View
def check_signup(request):
    total_users = CustomUser.objects.count()
    is_signup_allowed = total_users < 11  # Check if signup is allowed based on the user count
    return JsonResponse({'is_signup_allowed': is_signup_allowed})
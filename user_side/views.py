from django.shortcuts import render,redirect

# Create your views here.
def home(request):
    user=request.user
    return render(request,'home.html',{'user':user})
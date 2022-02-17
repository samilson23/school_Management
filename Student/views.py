from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from Student.EmailBackend import EmailBackend


def home(request):
    return render(request,"index.html",{})


def showLoginPage(request):
    return render(request,"login.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h1>METHOD NOT ALLOWED</h1>")   
    else:
        user =EmailBackend.authenticate(request, username=request.POST.get("email"),password=request.POST.get("password"),usertype=request.POST.get("user_type"))
        if user!= None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"Invalid Login Credentials")
            return HttpResponseRedirect("/")

def GetUserDetails(request):
    if request.user!= None:
        return HttpResponse("user :" + request.user.email + " usertype :" + request.user.user_type)
    return HttpResponse("please login first")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")



        # Create your views here.

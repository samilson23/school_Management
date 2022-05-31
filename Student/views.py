from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from Student.EmailBackend import EmailBackend
import requests

from Student.models import staff


def showLoginPage(request):
    return render(request,"login.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h1>METHOD NOT ALLOWED</h1>")   
    else:
        user = EmailBackend.authenticate(request, username=request.POST.get("email"),password=request.POST.get("password"))
        if user!= None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/home')
            elif user.user_type=="2":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "3":
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

def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
           'var firebaseConfig = {' \
           '        apiKey: "AIzaSyDyVvdRphCt00sjukOFmFEJa_k8i3-LOyg",' \
           '        authDomain: "schoolmanagement-f3059.firebaseapp.com",' \
           '        databaseURL: "schoolmanagement-f3059-default-rtdb.firebaseio.com/",' \
           '        projectId: "schoolmanagement-f3059",' \
           '        storageBucket: "schoolmanagement-f3059.appspot.com",' \
           '        messagingSenderId: "14567271614",' \
           '        appId: "1:14567271614:web:4bbf4bba7fcd4fcfd642ef",' \
           '        measurementId: "G-XEFYCXVJZZ" ' \
           ' };' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
           'messaging.setBackgroundMessageHandler(function (payload) {' \
           '    console.log(payload);' \
           '    const notification=JSON.parse(payload);' \
           '    const notificationOption={' \
           '        body:notification.body,' \
           '        icon:notification.icon' \
           '    };' \
           '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'

    return HttpResponse(data,content_type="text/javascript")




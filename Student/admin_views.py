import django_filters.filters
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from Student.filters import HodFilter, StaffFilter, StudentFilter
from Student.models import CustomUser, hod, staff, students, attendancereport, units_registration, leavereportstudent, \
    feedbackstudent, notificationstudent, StudentResult, subject


def home(request):
    return render(request,"admin_template/home.html")

def add_hod(request):
    return render(request,"admin_template/add_hod.html")

def add_hod_save(request):
    if request.method!='POST':
        return HttpResponse("Method not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")

        try:
            user = CustomUser.objects.create_user(username=user_name, email=email,
                                                  first_name=first_name, last_name=last_name, user_type=2)
            user.hod.address = address
            user.set_password("changeme")
            user.save()
            messages.success(request, "Successfully Added HOD")
            return HttpResponseRedirect(reverse("add_hod"))
        except:
            messages.error(request, "Failed to add Hod")
            return HttpResponseRedirect(reverse("add_hod"))

def manage_hod(request):
    HOD = hod.objects.all()
    Myfilter = HodFilter(request.GET, queryset=HOD)
    HOD=Myfilter.qs
    context={
        'HOD':HOD,
        'Myfilter':Myfilter.form
    }
    return render(request,'admin_template/manage_hod.html',context)


def delete_hod(request,pk):
    obj = hod.objects.get(pk=pk)
    if request.method=="POST":
        obj.delete()
        return HttpResponseRedirect(reverse('manage_hod'))
    return render(request,"admin_template/delete.html",{"obj":obj})

def Staff(request):
    staf = staff.objects.all()
    filterstaf = StaffFilter(request.GET,queryset=staf)
    staf = filterstaf.qs
    paginator = Paginator(staf, 10)
    page = request.GET.get('page',1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page,on_each_side=3,on_ends=2)
    try:
        staf = paginator.page(page)
    except PageNotAnInteger:
        staf = paginator.page(1)
    except EmptyPage:
        staf = paginator.page(paginator.num_pages)
    context = {
        'staf':staf,
        'filterstaf':filterstaf.form,
        'page_obj':page_obj,
        'page_range':page_range
    }
    return render(request,'admin_template/manage_staff.html',context)

def delete_staff(request,pk):
    staf = staff.objects.get(pk=pk)
    if request.method=="POST":
        staf.delete()
        return HttpResponseRedirect(reverse('Staff'))
    return render(request,"admin_template/delete_staff.html",{"staf":staf})

def Student(request):
    student = students.objects.all()
    filters = StudentFilter(request.GET,queryset=student)
    student = filters.qs
    page = request.GET.get('page',1)
    paginator = Paginator(student,10)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page,on_each_side=3,on_ends=2)
    try:
        student = paginator.page(page)
    except PageNotAnInteger:
        student = paginator.page(1)
    except EmptyPage:
        student = paginator.page(paginator.num_pages)
    context = {
        'student':student,
        'page_obj':page_obj,
        'page_range':page_range,
        'filters':filters.form
    }
    return render(request,'admin_template/manage_students.html',context)


def delete_student(request,id):
    student = students.objects.get(admin=id)
    context={
        "student":student
    }
    if request.method == "POST":
        student.delete()
        return HttpResponseRedirect(reverse('Student'))
    return render(request,"admin_template/delete_student.html",context)


def staff_edit(request,staff_id ):
    admin_staff = staff.objects.get(admin=staff_id)
    return render(request,"admin_template/staff_edit.html",{"admin_staff":admin_staff,"id":staff_id})

def staff_edit_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        password = request.POST.get("password")
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.set_password("changeme")
            user.save()
            messages.success(request, "Successfully Saved Staff")
            return HttpResponseRedirect(reverse("staff_edit",kwargs={"staff_id":staff_id}))
        except :
            messages.error(request, "Failed to Save Staff")
            return HttpResponseRedirect(reverse("staff_edit",kwargs={"staff_id":staff_id}))


def student_edit(request,student_id ):
    admin_student = students.objects.get(admin=student_id)
    return render(request,"admin_template/student_edit.html",{"admin_student":admin_student,"id":student_id})

def student_edit_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.POST.get("student_id")
        password = request.POST.get("password")
        try:
            user = CustomUser.objects.get(id=student_id)
            user.set_password("changeme")
            user.save()
            messages.success(request, "Successfully Updated Student")
            return HttpResponseRedirect(reverse("student_edit",kwargs={"student_id":student_id}))
        except :
            messages.error(request, "Failed to Update Student")
            return HttpResponseRedirect(reverse("student_edit",kwargs={"student_id":student_id}))

def hod_edit(request,hod_id):
    admin_hod = hod.objects.get(admin=hod_id)
    return render(request,"admin_template/hod_edit.html",{"admin_hod":admin_hod,"id":hod_id})

def hod_edit_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        hod_id = request.POST.get("hod_id")
        password = request.POST.get("password")
        try:
            user = CustomUser.objects.get(id=hod_id)
            user.set_password("changeme")
            user.save()
            messages.success(request, "Successfully Updated Hod")
            return HttpResponseRedirect(reverse("hod_edit",kwargs={"hod_id":hod_id}))
        except :
            messages.error(request, "Failed to Update Hod")
            return HttpResponseRedirect(reverse("hod_edit",kwargs={"hod_id":hod_id}))






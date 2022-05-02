import django_filters.filters
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from Student.filters import HodFilter, StaffFilter, StudentFilter
from Student.models import CustomUser, hod, staff, students


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
            user = CustomUser.objects.create_user(username=user_name, email=email, password=password,
                                                  first_name=first_name, last_name=last_name, user_type=2)
            user.hod.address = address
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

def delete_hod(request,id):
    Hod=hod.objects.get(admin=id)
    user = CustomUser.objects.get(id=id)
    Hod.delete()
    user.delete()

    return HttpResponseRedirect(reverse('manage_hod'))

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

def delete_staff(request,id):
    staf = staff.objects.get(admin=id)
    user = CustomUser.objects.get(id=id)
    staf.delete()
    user.delete()

    return HttpResponseRedirect(reverse('Staff'))

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
    user = CustomUser.objects.get(id=id)
    user.delete()
    student.delete()

    return HttpResponseRedirect(reverse('Student'))








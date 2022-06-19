import django_filters.filters
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from Student.filters import HodFilter, StaffFilter, StudentFilter, SchoolFilter, DeptFilter
from Student.models import CustomUser, hod, staff, students, attendancereport, leavereportstudent, \
    feedbackstudent, notificationstudent, StudentResult, subject, courses, attendance, leavereportstaff, school, \
    department


def home(request):
    student_count = students.objects.all().count()
    hod_count = hod.objects.all().count()
    staff_count1 = staff.objects.all().count()
    staff_count = int(staff_count1)-1
    course_count = courses.objects.all().count()
    subject_count = subject.objects.all().count()
    subjects = subject.objects.all()
    school_count = school.objects.all().count


    course_all = courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_in_course_list = []
    for course in course_all:
        Subjects = subject.objects.filter(course_id=course.id).count()
        Students = students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(Subjects)
        student_count_in_course_list.append(Students)

    subject_list = []
    student_count_in_subject_list = []
    subjects_all = subject.objects.all()
    for Subject in subjects_all:
        course = courses.objects.get(id=Subject.course_id.id)
        students_count = subject.objects.filter(course_id=course.id).count()
        subject_list.append(Subject.subject_name)
        student_count_in_subject_list.append(students_count)

    attendance_absent_list_staff = []
    attendance_present_list_staff = []
    staff_name_list = []
    staffs = staff.objects.all()
    for Staff in staffs:
        subject_ids = subject.objects.filter(staff_id=Staff.admin.id)
        Attendance = attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves = leavereportstaff.objects.filter(staff_id=Staff.id, leave_status=1).count()
        attendance_present_list_staff.append(Attendance)
        attendance_absent_list_staff.append(leaves)
        if Staff.admin.id == 3:
            pass
        else:
            staff_name_list.append(Staff.admin.username)
    schools = school.objects.all()
    Myfilter = SchoolFilter(request.GET, queryset=schools)
    schools = Myfilter.qs

    attendance_absent_list_student = []
    attendance_present_list_student = []
    attendance_leave_list_student = []
    student_name_list = []
    Student_all = students.objects.all()
    for student in Student_all:
        present = attendancereport.objects.filter(student_id=student.id, status=True).count()
        Absent = attendancereport.objects.filter(student_id=student.id, status=False).count()
        leaves = leavereportstudent.objects.filter(student_id=student.id, leave_status=1).count()
        attendance_present_list_student.append(present)
        attendance_absent_list_student.append(Absent)
        attendance_leave_list_student.append(leaves)
        student_name_list.append(student.admin.username)

    school_all = school.objects.all()
    school_name_list = []
    department_count_list = []
    for schools in school_all:
        departments = department.objects.filter(school_id=schools.id).count()
        school_name_list.append(schools.school_name)
        department_count_list.append(departments)

    context={
        "school_name_list":school_name_list,
        "department_count_list":department_count_list,
        "student_count": student_count,
         "hod_count": hod_count,
         "staff_count": staff_count,
         "course_count": course_count,
         "school_count": school_count,
         "subject_count": subject_count,
         "course_name_list": course_name_list,
         "subject_count_list": subject_count_list,
         "student_count_in_course_list": student_count_in_course_list,
         "subject_list": subject_list,
        "Myfilter": Myfilter.form,
        "schools":schools,
         "student_count_in_subject_list": student_count_in_subject_list,
         "attendance_present_list_staff": attendance_present_list_staff,
         "staff_name_list": staff_name_list,
         "attendance_absent_list_student": attendance_absent_list_student,
         "attendance_present_list_student": attendance_present_list_student,
         "student_name_list": student_name_list,
         "attendance_leave_list_student": attendance_leave_list_student,
         "attendance_absent_list_staff": attendance_absent_list_staff,
         "subjects": subjects
    }
    return render(request,
                  "admin_template/home.html",context)


def add_hod(request):
    Sch = department.objects.all()
    HOD = hod.objects.all()
    Myfilter = HodFilter(request.GET, queryset=HOD)
    HOD = Myfilter.qs
    paginator = Paginator(HOD, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        HOD = paginator.page(page)
    except PageNotAnInteger:
        HOD = paginator.page(1)
    except EmptyPage:
        HOD = paginator.page(paginator.num_pages)
    context = {
        'HOD': HOD,
        'Myfilter': Myfilter.form,
        'page_obj': page_obj,
        'page_range': page_range,
        'Sch':Sch
    }
    return render(request,"admin_template/add_hod.html",context)

def add_hod_save(request):
    if request.method!='POST':
        return HttpResponse("Method not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        dept_id = request.POST.get("school")
        address = request.POST.get("address")

        try:
            dept = department.objects.get(id=dept_id)
            if email=="":
                user = CustomUser.objects.create_user(username=user_name, email=email,
                                                      first_name=first_name, last_name=last_name, user_type=2)
                user.hod.address = address
                user.hod.dept_id = dept
                user.set_password("changeme")
                user.save()
            else:
                user = CustomUser.objects.create_user(username=user_name, email=email,
                                                      first_name=first_name, last_name=last_name, user_type=2)
                user.hod.address = address
                user.hod.dept_id = dept
                user.set_password("changeme")
                user.save()
            messages.success(request, "Successfully Added HOD")
            return HttpResponseRedirect(reverse("add_hod"))
        except:
            messages.error(request, "Failed to add Hod")
            return HttpResponseRedirect(reverse("add_hod"))

def add_school(request):
    schools = school.objects.all()
    Myfilter = SchoolFilter(request.GET, queryset=schools)
    schools = Myfilter.qs
    paginator = Paginator(schools, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        schools = paginator.page(page)
    except PageNotAnInteger:
        schools = paginator.page(1)
    except EmptyPage:
        schools = paginator.page(paginator.num_pages)
    context={
        "schools":schools,
        'Myfilter': Myfilter.form,
        'page_obj': page_obj,
        'page_range': page_range,
    }
    return render(request,"admin_template/add_school.html",context)

def add_school_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        course = request.POST.get("school")
        try:
            if course!="":
                school_model = school(school_name=course)
                school_model.save()
                messages.success(request, "Successfully Added School")
            return HttpResponseRedirect(reverse("add_school"))
        except:
            if course!="":
                messages.error(request, "Failed To Add School")
            return HttpResponseRedirect(reverse("add_school"))

def add_department(request):
    Sch = school.objects.all()
    departments = department.objects.all()
    Myfilter = DeptFilter(request.GET, queryset=departments)
    departments = Myfilter.qs
    paginator = Paginator(departments, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        departments = paginator.page(page)
    except PageNotAnInteger:
        departments = paginator.page(1)
    except EmptyPage:
        departments = paginator.page(paginator.num_pages)
    context={"Sch": Sch,
             "departments":departments,
             'Myfilter': Myfilter.form,
             'page_obj': page_obj,
             'page_range': page_range,
         }
    return render(request,"admin_template/add_dept.html", context)

def add_dept_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        dept = request.POST.get("dept")
        Schools = request.POST.get("dept1")
        try:
            if dept!="":
                School_id = school.objects.get(id=Schools)
                dept_model = department(dept_name=dept,school_id=School_id)
                dept_model.save()
                messages.success(request, "Successfully Added Department")
            return HttpResponseRedirect(reverse("add_department"))
        except:
            if dept!="":
                messages.error(request, "Failed To Add Department")
            return HttpResponseRedirect(reverse("add_department"))

def manage_hod(request):
    HOD = hod.objects.all()
    Myfilter = HodFilter(request.GET, queryset=HOD)
    HOD=Myfilter.qs
    paginator = Paginator(HOD, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        HOD = paginator.page(page)
    except PageNotAnInteger:
        HOD = paginator.page(1)
    except EmptyPage:
        HOD = paginator.page(paginator.num_pages)
    context={
        'HOD':HOD,
        'Myfilter':Myfilter.form,
        'page_obj':page_obj,
        'page_range':page_range
    }
    return render(request,'admin_template/manage_hod.html',context)


def delete_hod(request,id):
    obj = hod.objects.get(admin=id)
    hod_obj = CustomUser.objects.get(id=id)
    if request.method=="POST":
        obj.delete()
        hod_obj.delete()
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

def delete_staff(request,id):
    student = staff.objects.get(admin=id)
    customuser = CustomUser.objects.get(id=id)
    context = {
        "student": student
    }
    if request.method == "POST":
        student.delete()
        customuser.delete()
        return HttpResponseRedirect(reverse('Staff'))
    return render(request,"admin_template/delete_staff.html",context)

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
    customuser = CustomUser.objects.get(id=id)
    context={
        "student":student
    }
    if request.method == "POST":
        student.delete()
        customuser.delete()

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


def Admin(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "admin_template/admin_profile.html", {"user": user})


def admin_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Changed")
            return HttpResponseRedirect(reverse("Admin"))
        except:
            messages.error(request, " Failed To Change Profile ")
            return HttpResponseRedirect(reverse("Admin"))

def edit_school(request,id):
    schools = school.objects.get(id=id)
    return render(request,"admin_template/schools.html",{"schools":schools})

def edit_school_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        schools = request.POST.get("school")
        school_id = request.POST.get("sch1")
        try:
            course = school.objects.get(id=school_id)
            course.school_name = schools
            course.save()
            messages.success(request, "School Updated")
            return HttpResponseRedirect(reverse("edit_school",kwargs={"id":school_id}))
        except:
            messages.error(request, "School Not Saved")
            return HttpResponseRedirect(reverse("edit_school",kwargs={"id":school_id}))

def edit_dept(request,id):
    schools = department.objects.get(id=id)
    return render(request,"admin_template/dept.html",{"schools":schools})

def edit_dept_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        schools = request.POST.get("school")
        school_id = request.POST.get("sch1")
        try:
            course = department.objects.get(id=school_id)
            course.dept_name = schools
            course.save()
            messages.success(request, "Department Updated")
            return HttpResponseRedirect(reverse("edit_dept",kwargs={"id":school_id}))
        except:
            messages.error(request, "Department Not Saved")
            return HttpResponseRedirect(reverse("edit_dept",kwargs={"id":school_id}))
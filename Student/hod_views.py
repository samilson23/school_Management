import datetime
from email import message
import json

import requests
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from Student import admin
from Student.forms import EditStudentForm
from Student.models import CustomUser, attendance, attendancereport, courses, feedbackstaff, feedbackstudent, \
    leavereportstaff, leavereportstudent, notificationstaff, notificationstudent, staff, subject, students, \
    sessionmodel, semester, unitregistration, registrationreport, StudentResult
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .filters import CourseFilter, SubjectFilter, StudentFilter, StaffFilter, StudentFeedbackFilter, \
    StaffFeedbackFilter, StaffNotificationFilter
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def admin_home(request):
    student_count=students.objects.all().count()
    staff_count1 = staff.objects.all().count()
    staff_count = int(staff_count1) - 1
    course_count=courses.objects.all().count()
    subject_count=subject.objects.all().count()

    course_all=courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_in_course_list=[]
    for course in course_all:
        Subjects=subject.objects.filter(course_id=course.id).count()
        Students=students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(Subjects)
        student_count_in_course_list.append(Students)



    subject_list=[]
    student_count_in_subject_list=[]
    subjects_all = subject.objects.all()
    for Subject in subjects_all:
       course=courses.objects.get(id=Subject.course_id.id)
       students_count=subject.objects.filter(course_id=course.id).count()
       subject_list.append(Subject.subject_name)
       student_count_in_subject_list.append(students_count)


    attendance_absent_list_staff=[]
    attendance_present_list_staff=[]
    staff_name_list=[]
    staffs = staff.objects.all()
    for Staff in staffs:
        subject_ids=subject.objects.filter(staff_id=Staff.admin.id)
        Attendance=attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves=leavereportstaff.objects.filter(staff_id=Staff.id,leave_status=1).count()
        attendance_present_list_staff.append(Attendance)
        attendance_absent_list_staff.append(leaves)
        if Staff.admin.id == 3:
            pass
        else:
            staff_name_list.append(Staff.admin.username)


    attendance_absent_list_student=[]
    attendance_present_list_student=[]
    attendance_leave_list_student=[]
    student_name_list=[]
    Student_all = students.objects.all()
    for student in Student_all:
        present=attendancereport.objects.filter(student_id=student.id,status=True).count()
        Absent=attendancereport.objects.filter(student_id=student.id,status=False).count()
        leaves=leavereportstudent.objects.filter(student_id=student.id,leave_status=1).count()
        attendance_present_list_student.append(present)
        attendance_absent_list_student.append(Absent)
        attendance_leave_list_student.append(leaves)
        student_name_list.append(student.admin.username)

    subjects=subject.objects.all()
    context={
        "student_count":student_count,
         "staff_count":staff_count,
         "course_count":course_count,
         "subject_count":subject_count,
         "course_name_list":course_name_list,
         "subject_count_list":subject_count_list,
         "student_count_in_course_list":student_count_in_course_list,
         "subject_list":subject_list,
         "student_count_in_subject_list":student_count_in_subject_list,
         "attendance_present_list_staff":attendance_present_list_staff,
         "staff_name_list":staff_name_list,
         "attendance_absent_list_student":attendance_absent_list_student,
         "attendance_present_list_student":attendance_present_list_student,
         "student_name_list":student_name_list,
         "attendance_leave_list_student":attendance_leave_list_student,
         "attendance_absent_list_staff":attendance_absent_list_staff,
         "subjects":subjects
    }
    return render(request,
                  "Hod_template/home_content.html",context)


def add_staff(request):
    subjects = subject.objects.all()
    return render(request,"Hod_template/add_staff_template.html",{"subjects":subjects})
def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        subject_id = request.POST.get("subject")
        address = request.POST.get("address")
        try:
            if email=="":
                user = CustomUser.objects.create_user(username=user_name,email=email,first_name=first_name, last_name=last_name,user_type=3)
                user.set_password('changeme')
                user.staff.address = address
                # subjectss = subject.objects.get(id=subject_id)
                # user.staff.subject_id=subjectss
                user.save()
            else:
                user = CustomUser.objects.create_user(username=user_name, email=email, first_name=first_name,
                                                      last_name=last_name, user_type=3)
                user.set_password('changeme')
                user.staff.address = address
                # subjectss = subject.objects.get(id=subject_id)
                # user.staff.subject_id=subjectss
                user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "Failed to add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_course(request):
    return render(request, "Hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        course = request.POST.get("course_name")
        try:
            course_model = courses(course_name=course)
            course_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request, "Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))
def add_student(request):
    course=courses.objects.all()
    sessions=sessionmodel.objects.all()
    return render(request, "Hod_template/add_student_template.html",{"course":course,"sessions":sessions})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        # password = request.POST.get("password")
        address = request.POST.get("address")
        session_year_id = request.POST.get("session")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")

        try:
            if email=="":
                user = CustomUser.objects.create_user(username=username, email=email,
                                                      first_name=first_name, last_name=last_name, user_type=4)
                user.students.address = address
                course_obj = courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                session = sessionmodel.objects.get(id=session_year_id)
                user.students.session_year_id = session
                user.students.gender = sex
                user.set_password("changeme")
                user.save()
            else:
                user = CustomUser.objects.create_user(username=username, email=email,
                                                      first_name=first_name, last_name=last_name, user_type=4)
                user.students.address = address
                course_obj = courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                session = sessionmodel.objects.get(id=session_year_id)
                user.students.session_year_id = session
                user.students.gender = sex
                user.set_password("changeme")
                user.save()
            messages.success(request, "Successfully Added Student")
            return HttpResponseRedirect(reverse("add_student"))

        except:
            messages.error(request, "Failed to add Student")
            return HttpResponseRedirect(reverse("add_student"))

def add_subject(request):
    course = courses.objects.all()
    Stage = semester.objects.all()
    Staff = CustomUser.objects.filter(user_type=3)
    return render(request, "Hod_template/add_subject_template.html", {"Staff": Staff,"course": course,"Stage":Stage})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h1>Method Not Allowed</h1>")
    else:
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        course = courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        code = request.POST.get("code")
        stage_id = request.POST.get("stage")
        stage = semester.objects.get(id=stage_id)
        staff = CustomUser.objects.get(id=staff_id)

        # try:
        subjects = subject(subject_name=subject_name,course_id=course,stage_id=stage,staff_id=staff,code=code)
        subjects.save()
        messages.success(request, "Successfully Added Subject")
        return HttpResponseRedirect(reverse("add_subject"))
    # except:
        messages.error(request, "Subject Not Added")
        return HttpResponseRedirect(reverse("add_subject"))


# def add_subject_save(request):
#     if request.method!="POST":
#         return HttpResponse("<h2>Method Not Allowed</h2>")
#     else:
#         subject_name=request.POST.get("subject_name")
#         course_id=request.POST.get("course")
#         course=courses.objects.get(id=course_id)
#         staff_id=request.POST.get("staff")
#         staff=CustomUser.objects.get(id=staff_id)
#
#         try:
#             subjects=subject(subject_name=subject_name,course_id=course,staff_id=staff)
#             subjects.save()
#             messages.success(request,"Successfully Added Subject")
#             return HttpResponseRedirect(reverse("add_subject"))
#         except:
#             messages.error(request,"Failed to Add Subject")
#             return HttpResponseRedirect(reverse("add_subject"))

def manage_staff(request):
    staf = staff.objects.all()
    filterstaf = StaffFilter(request.GET, queryset=staf)
    staf = filterstaf.qs
    paginator = Paginator(staf,10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        staf = paginator.page(page)
    except PageNotAnInteger:
        staf = paginator.page(1)
    except EmptyPage:
        staf = paginator.page(paginator.num_pages)
    context={
        'staf':staf,
        'page_obj':page_obj,
        'page_range':page_range,
        "filterstaf":filterstaf.form
    }
    return render(request, "Hod_template/manage_staff_template.html",context)

def manage_student(request):
    student = students.objects.all()
    filters = StudentFilter(request.GET, queryset=student)
    student = filters.qs
    paginator = Paginator(student,10)
    page = request.GET.get('page',1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page,on_each_side=3,on_ends=2)
    try:
        student = paginator.page(page)
    except PageNotAnInteger:
        student = paginator.page(1)
    except EmptyPage:
        student = paginator.page(paginator.num_pages)

    context = {
        "student": student,
        "page_obj": page_obj,
        "page_range": page_range,
        "filters":filters.form
    }
    return render(request, "Hod_template/manage_student_template.html",context)

def manage_course(request):
    course = courses.objects.all()
    Myfilter = CourseFilter(request.GET, queryset=course)
    course=Myfilter.qs
    paginator = Paginator(course,10)
    page = request.GET.get('page',1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page,on_each_side=3,on_ends=2)
    try:
        course=paginator.page(page)
    except PageNotAnInteger:
        course = paginator.page(1)
    except EmptyPage:
        course = paginator.page(paginator.num_pages)
    context = {
                "course": course,
                "Myfilter":Myfilter.form,
                'page_obj':page_obj,
                'page_range':page_range
    }

    return render(request, "Hod_template/manage_course_template.html",context)

def manage_subjects(request):
    subjects = subject.objects.all()
    Myfilter = SubjectFilter(request.GET, queryset=subjects)
    subjects = Myfilter.qs
    paginator = Paginator(subjects, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        subjects = paginator.page(page)
    except PageNotAnInteger:
        subjects = paginator.page(1)
    except EmptyPage:
        subjects = paginator.page(paginator.num_pages)
    context= {
        "subjects": subjects,
        "Myfilter":Myfilter.form,
        "page_obj":page_obj,
        "page_range":page_range
    }
    return render(request, "hod_template/manage_subjects_template.html",context)

def edit_staff(request,staff_id):
    staffss = staff.objects.get(admin=staff_id)
    return render(request,"Hod_template/edit_staff_template.html",{"staffss": staffss,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            staff_model = staff.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, "Successfully Saved Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request, "Failed to Save Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_student(request,student_id):
    request.session['student_id']=student_id
    student=students.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.course_id.id
    # form.fields['profile_pic'].initial=student.profile_pic
    # form.fields['sex'].initial=student.gender
    form.fields['session_year_id'].initial=student.session_year_id.id
    return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect(reverse("manage_student"))

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            # sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None


            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=students.objects.get(admin=student_id)
                student.address=address
                session_year = sessionmodel.objects.get(id=session_year_id)
                student.session_year_id = session_year
                # student.gender=sex
                course=courses.objects.get(id=course_id)
                student.course_id=course
                if profile_pic_url!=None:
                    student.profile_pic=profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=students.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_subject(request,subject_id):
    subjects = subject.objects.get(id=subject_id)
    course = courses.objects.all()
    staff = CustomUser.objects.filter(user_type=3)
    return render(request,"Hod_template/edit_subject_template.html",{"subjects":subjects,"course":course,"staff":staff,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")

    try:
        subjects = subject.objects.get(id=subject_id)
        subjects.subject_name = subject_name
        staffs = CustomUser.objects.get(id=staff_id)
        subjects.staff_id=staffs
        course = courses.objects.get(id=course_id)
        subjects.course_id=course
        subjects.save()
        messages.success(request, "Successfully Edited Subject")
        return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
    except:
        messages.error(request, "Subject Not Saved")
        return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))

def edit_course(request,course_id):
    course = courses.objects.get(id=course_id)
    return render(request,"Hod_template/edit_course_template.html",{"course":course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course_name")
        try:
            course = courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, "Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        except:
            messages.error(request, "Course Not Saved")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))

def manage_session(request):
    return render(request,"Hod_template/manage_session_template.html")

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year = request.POST.get("session start")
        session_end_year = request.POST.get("session end")
        try:
            session_year = sessionmodel(session_start_year=session_start_year, session_end_year=session_end_year)
            session_year.save()
            messages.success(request, "Session Saved")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, " Failed To Save Session ")
            return HttpResponseRedirect(reverse("manage_session"))

@csrf_exempt
def check_user_email(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)         


@csrf_exempt
def check_subject_code(request):
    code=request.POST.get("code")
    sub_code=subject.objects.filter(code=code).exists()
    if sub_code:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def student_feedback_msg(request):
    feedbacks = feedbackstudent.objects.all().order_by("-created_at")
    filters = StudentFeedbackFilter(request.GET, queryset=feedbacks)
    feedbacks = filters.qs
    paginator = Paginator(feedbacks, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        feedbacks = paginator.page(page)
    except PageNotAnInteger:
        feedbacks = paginator.page(1)
    except EmptyPage:
        feedbacks = paginator.page(paginator.num_pages)

    context = {
        "feedbacks":feedbacks,
        "filters":filters.form,
        "page_range":page_range,
        "page_obj":page_obj
    }
    return render(request,"Hod_template/student_feedback_msg.html",context)


def staff_feedback_msg(request):
    feedback = feedbackstaff.objects.all().order_by("-created_at")
    filters = StaffFeedbackFilter(request.GET, queryset=feedback)
    feedback = filters.qs
    paginator = Paginator(feedback, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        feedback = paginator.page(page)
    except PageNotAnInteger:
        feedback = paginator.page(1)
    except EmptyPage:
        feedback = paginator.page(paginator.num_pages)

    context = {
        "feedback":feedback,
        "filters":filters.form,
        "page_range":page_range,
        "page_obj":page_obj
    }
    return render(request,"Hod_template/staff_feedback_msg.html",context)

@csrf_exempt
def student_feedback_msg_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=feedbackstudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False") 

@csrf_exempt
def staff_feedback_msg_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=feedbackstaff.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")   

def staff_leave_reply(request):
    staff_leaves=leavereportstaff.objects.all()
    return render(request,"Hod_template/staff_leave_reply.html",{"staff_leaves":staff_leaves})

def student_leave_reply(request):
    leaves=leavereportstudent.objects.all()
    return render(request,"Hod_template/student_leave_reply.html",{"leaves":leaves})


def student_approved_leave(request,leave_id):
    leave=leavereportstudent.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_reply"))

def student_disapproved_leave(request,leave_id):
    leave=leavereportstudent.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_reply"))   


def staff_approved_leave(request,leave_id):
    leave=leavereportstaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_reply"))

def staff_disapproved_leave(request,leave_id):
    leave=leavereportstaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_reply"))     

def admin_view_attendance(request):
    subjects=subject.objects.all()
    session_year_id=sessionmodel.objects.all()
    return render(request,"Hod_template/admin_view_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def admin_get_attendance_date(request):
    subjects=request.POST.get("subjects")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=subject.objects.get(id=subjects)
    session_year_obj=sessionmodel.objects.get(id=session_year_id)
    Attendance=attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in Attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    Attendance = attendance.objects.get(id=attendance_date)
    attendance_data=attendancereport.objects.filter(attendance_id=Attendance)
    list_data = []
    for student in attendance_data:
        data_small = {"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+"  "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"Hod_template/admin_profile.html",{"user":user})  


def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:    
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        email=request.POST.get("email")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                 customuser.set_password(password)
            if email != None and email != "":
                customuser.email = email
            customuser.save()
            messages.success(request, "Profile Changed")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, " Failed To Change Profile ")
            return HttpResponseRedirect(reverse("admin_profile"))    
            

def admin_send_notification_student(request):
    student = students.objects.all()
    filters = StudentFilter(request.GET, queryset=student)
    student = filters.qs
    paginator = Paginator(student, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        student = paginator.page(page)
    except PageNotAnInteger:
        student = paginator.page(1)
    except EmptyPage:
        student = paginator.page(paginator.num_pages)
    context = {
        "student": student,
        "page_obj": page_obj,
        "page_range": page_range,
        "filters": filters.form
    }
    return render(request,"Hod_template/student_notification.html",context)


def admin_send_notification_staff(request):
    staffs = staff.objects.all()
    filters = StaffFilter(request.GET, queryset=staffs)
    staffs = filters.qs
    paginator = Paginator(staffs, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        staffs = paginator.page(page)
    except PageNotAnInteger:
        staffs = paginator.page(1)
    except EmptyPage:
        staffs = paginator.page(paginator.num_pages)

    context = {
        "staffs":staffs,
        "page_obj":page_obj,
        "filters": filters.form,
        "page_range":page_range,
    }
    return render(request,"Hod_template/staff_notification.html",context)

@csrf_exempt
def send_student_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    student=students.objects.get(admin=id)
    Hod = CustomUser.objects.get(id=request.user.id)
    token = student.fcm_token  
    url="https://fcm.googleapis.com/fcm/send"  
    body={
        "notification":{
            "title":"Student Management System",
            "body":message,
            "click_action": "https://samilson.herokuapp.com/student_all_notification",
            "icon": "http://samilson.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=notificationstudent(student_id=student,message=message,Hod_id=Hod)
    notification.save()
    print(data.text)
    return HttpResponse("True")   

@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    staffs=staff.objects.get(admin=id)
    Hod = CustomUser.objects.get(id=request.user.id)
    token = staffs.fcm_token  
    url="https://fcm.googleapis.com/fcm/send"  
    body={
        "notification":{
            "title":"School Management System",
            "body":message,
            "click_action": "https://localhost:8000/staff_all_notification",
            "icon": "static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=AAAAA2RG7L4:APA91bGHQ0Q8L5rOI2uQbZDJgHOkpx2nkf4_IIcEcZhBWd-AXqYHBCCUHSibJYYu6MemU2aMza9ERk0t2HFG56hhQ8195OBjyq9JBHWnajPCKHkoFTWZl7Mq0sG_LmA6x3c44_TWkMSM"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=notificationstaff(staff_id=staffs, message=message, read=False,Hod_id=Hod)
    notification.save()
    print(data.text)
    return HttpResponse("True")


def datatable(request):
    return render(request,"Hod_template/datatable.html")

def update_student_units(request,id):
    student = students.objects.get(admin=id)
    student_obj = CustomUser.objects.get(id=id)
    Stage = unitregistration.objects.filter(student_id=student_obj)
    context={
        "student":student,
        "student_obj":student_obj,
        "Stage":Stage
    }
    return render(request,"Hod_template/update_registration.html",context)


@csrf_exempt
def get_unregistered_student_units(request):
    stage=request.POST.get("stage")
    student = request.POST.get("student_id")
    stage_id = unitregistration.objects.get(id=stage)
    student_id = CustomUser.objects.get(id=student)
    attendance_data = registrationreport.objects.filter(student_id=student_id,unit_id=stage_id)
    list_data = []
    for student in attendance_data:
            data_small = {"id": student.subject_id.id,
                          "name": student.subject_id.subject_name,
                          "code":student.subject_id.code,
                          "status": student.status}
            list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def save_update_student_units(request):
    student_ids = request.POST.get("student_ids")
    stage = request.POST.get("stage")
    student = request.POST.get("student_id")
    stage_id = unitregistration.objects.get(id=stage)
    json_student = json.loads(student_ids)
    try:
        for stud in json_student:
            Subject = subject.objects.get(id=stud['id'])
            student_id = CustomUser.objects.get(id=student)
            attendance_report = registrationreport.objects.get(student_id=student_id,unit_id=stage_id,subject_id=Subject)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("saved")
    except:
        return HttpResponse("not saved")


from datetime import datetime
import json
from uuid import uuid4

from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa

from Student.filters import StaffLeaveFilter
from Student.models import Adminhod, CustomUser, OnlineClassRoom, StudentResult, attendance, attendancereport, courses, \
    leavereportstaff, notificationstaff, staff, subject, sessionmodel, students, \
    feedbackstaff, registrationreport, department, semester
from django.contrib import messages

def staff_home(request):
    staff_obj = staff.objects.get(admin=request.user.id)
    notifications = notificationstaff.objects.filter(staff_id=staff_obj.id,read=False).count()
    notification = notificationstaff.objects.filter(staff_id=staff_obj.id,read=False)
    Subjects=subject.objects.filter(staff_id=request.user.id)
    course_id_list=[]
    for Subject in Subjects:
        course=courses.objects.get(id=Subject.course_id.id)
        course_id_list.append(course.id)

    final_course=[]
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)  
    student_count=students.objects.filter(course_id__in=final_course).count()

    Attendance_count=attendance.objects.filter(subject_id__in=Subjects).count()
    Staff=staff.objects.get(admin=request.user.id)
    leave_count=leavereportstaff.objects.filter(staff_id=Staff.id,leave_status=1).count()
    subject_count=Subjects.count()
    
    subject_list=[]
    attendance_list=[]
    for Subject in Subjects:
        Attendance_count1=attendance.objects.filter(subject_id=Subject.id).count()
        subject_list.append(Subject.code)
        attendance_list.append(Attendance_count1)

    student_attendance=students.objects.filter(course_id__in=final_course)
    student_list=[]   
    student_list_attendance_present=[]
    student_list_attendance_absent=[]
    for student in student_attendance:
        Attendance_present_count=attendancereport.objects.filter(status=True,student_id=student.id).count()
        Attendance_absent_count=attendancereport.objects.filter(status=False,student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(Attendance_present_count)
        student_list_attendance_absent.append(Attendance_absent_count)
    return render(request,"staff_template/staff_home_template.html",{"notification":notification,"notifications":notifications,"student_count":student_count,"Attendance_count":Attendance_count,"leave_count":leave_count,"subject_count":subject_count,"subject_list":subject_list,"attendance_list":attendance_list,"student_list":student_list,"present_list":student_list_attendance_present,"staff_obj":staff_obj,"absent_list":student_list_attendance_absent})

def staff_take_attendance(request):
    subjects = subject.objects.filter(staff_id=request.user.id)
    session_years = sessionmodel.objects.all()
    staff_obj = staff.objects.get(admin=request.user.id)
    notifications = notificationstaff.objects.filter(staff_id=staff_obj.id,read=False).count()
    notification = notificationstaff.objects.filter(staff_id=staff_obj.id, read=False)
    return render(request,"staff_template/staff_take_attendance.html",{"notification":notification,"notifications":notifications,"subjects":subjects,"session_years":session_years})

@csrf_exempt
def get_students(request):
    subject_id=request.POST.get("subjects")
    session_year = request.POST.get("session_year")

    Subject = subject.objects.get(id=subject_id)
    session_model = sessionmodel.objects.get(id=session_year)
    student = students.objects.filter(course_id=Subject.course_id,session_year_id=session_model)
    list_data = []
    for student in student:
        data_small = {"id":student.admin.id,"name":student.admin.username+""}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def get_student(request):
    subject_id=request.POST.get("subjects")
    session_year = request.POST.get("session_year")

    Subject = subject.objects.get(id=subject_id)
    session_model = sessionmodel.objects.get(id=session_year)
    student = students.objects.filter(course_id=Subject.course_id,session_year_id=session_model)
    list_data = []
    for student in student:
        std=registrationreport.objects.filter(student_id=student.admin.id,status=1,subject_id=Subject).exists()
        if std:
            data_small = {"id":student.admin.id,"name":student.admin.username+""}
            list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt    
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids") 
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")
    subject_model = subject.objects.get(id=subject_id)
    session_model = sessionmodel.objects.get(id=session_year_id)
    json_student = json.loads(student_ids)
    try:
        Attendance=attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_model)
        Attendance.save()
        for stud in json_student:
            student = students.objects.get(admin=stud['id'])
            semesters = semester.objects.get(id=subject_model.stage_id.id)
            attendance_report=attendancereport(student_id=student,attendance_id=Attendance,status=stud['status'],stage_id=semesters)
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_update_attendance(request):
    subjects = subject.objects.filter(staff_id=request.user.id)
    session_year_id = sessionmodel.objects.all()
    staff_obj = staff.objects.get(admin=request.user.id)
    notifications = notificationstaff.objects.filter(staff_id=staff_obj.id,read=False).count()
    notification = notificationstaff.objects.filter(staff_id=staff_obj.id,read=False)
    return render(request,"staff_template/update_attendance.html",{"notification":notification,"subjects":subjects,"session_year_id":session_year_id,"notifications":notifications})

@csrf_exempt
def get_attendance_date(request):
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
def get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    Attendance = attendance.objects.get(id=attendance_date)
    attendance_data=attendancereport.objects.filter(attendance_id=Attendance)
    list_data = []
    for student in attendance_data:
        data_small = {"id":student.student_id.admin.id,"name":student.student_id.admin.username,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt    
def save_updateattendance_student(request): 
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    Attendance=attendance.objects.get(id=attendance_date)
    json_student = json.loads(student_ids)
    try:
        for stud in json_student:
            student = students.objects.get(admin=stud['id'])
            attendance_report=attendancereport.objects.get(student_id=student,attendance_id=Attendance)
            attendance_report.status=stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_apply_leave(request):
    staff_obj = staff.objects.get(admin=request.user.id)
    leave_data=leavereportstaff.objects.filter(staff_id=staff_obj).order_by('-id')
    notifications = notificationstaff.objects.filter(staff_id=staff_obj.id,read=False).count()
    notification = notificationstaff.objects.filter(staff_id=staff_obj.id,read=False)
    leave_stats = leavereportstaff.objects.all()
    Myfilter = StaffLeaveFilter(request.GET, queryset=leave_stats)
    leave_stats = Myfilter.qs
    paginator = Paginator(leave_data, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        leave_data = paginator.page(page)
    except PageNotAnInteger:
        leave_data = paginator.page(1)
    except EmptyPage:
        leave_data = paginator.page(paginator.num_pages)
    return render(request,"staff_template/staff_apply_leave.html",{"notification":notification,
                                                                   "leave_data":leave_data,"notifications":notifications,
                                                                   "leave_stats":leave_stats,
                                                                   'Myfilter': Myfilter.form,
                                                                   "page_range":page_range,
                                                                   "page_obj":page_obj
                                                                   })


def staff_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")  
        leave_msg=request.POST.get("leave_msg")
        staff_obj = staff.objects.get(admin=request.user.id)
        try:
            if leave_msg!="":
                dept_id = department.objects.get(id=staff_obj.dept_id.id)
                leave_report=leavereportstaff(staff_id=staff_obj,dept_id=dept_id,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
                leave_report.save()
                messages.success(request,"Successfully Applied For Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
             messages.error(request, "Failed To Apply For Leave")
             return HttpResponseRedirect(reverse("staff_apply_leave"))




def staff_feedback(request):
    staff_obj = staff.objects.get(admin=request.user.id)
    feedback_data = feedbackstaff.objects.filter(staff_id=staff_obj).order_by('-id')
    # Myfilter = (request.GET, queryset=HOD)
    # HOD = Myfilter.qs
    paginator = Paginator(feedback_data, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        feedback_data = paginator.page(page)
    except PageNotAnInteger:
        feedback_data = paginator.page(1)
    except EmptyPage:
        feedback_data = paginator.page(paginator.num_pages)
    notifications = notificationstaff.objects.filter(staff_id=staff_obj.id,read=False).count()
    notification = notificationstaff.objects.filter(staff_id=staff_obj.id,read=False)

    context={
        "notification":notification,
        "feedback_data":feedback_data,
        "notifications":notifications,
        "page_obj":page_obj,
        "page_range":page_range
    }
    return render(request,"staff_template/staff_feedback.html",context)


def staff_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_feedback"))
    else:
        feedback_msg = request.POST.get("feedback_msg")
        staff_obj = staff.objects.get(admin=request.user.id)
        if feedback_msg!="":
            try:
                dept_id=department.objects.get(id=staff_obj.dept_id.id)
                feedback_obj = feedbackstaff(staff_id=staff_obj,dept_id=dept_id,feedback=feedback_msg,feedback_reply="",status=0)
                feedback_obj.save()
                messages.success(request, "Complain Submitted")
                return HttpResponseRedirect(reverse("staff_feedback"))
            except:
                messages.error(request, "Failed To Submit Feedback")
                return HttpResponseRedirect(reverse("staff_feedback"))
        else:
            return HttpResponseRedirect(reverse("staff_feedback"))

def staff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    staffs=staff.objects.get(admin=user)
    notifications = notificationstaff.objects.filter(staff_id=staffs.id,read=False).count()
    notification = notificationstaff.objects.filter(staff_id=staffs.id,read=False)
    return render(request,"staff_template/staff_profile.html",{"notification":notification,"user":user,"staffs":staffs,"notifications":notifications})


def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:    
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        email=request.POST.get("email")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password != None and password!="":
                customuser.set_password(password)
            if email !=None and email != "":
                customuser.email = email
            customuser.save()
            staffs=staff.objects.get(admin=customuser)
            staffs.address=address
            staffs.save()
            if password!=None and password!="":
                customuser.set_password(password)
            messages.success(request, "Profile Changed")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, " Failed To Change Profile ")
            return HttpResponseRedirect(reverse("staff_profile"))   

@csrf_exempt
def staff_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        staffs=staff.objects.get(admin=request.user.id)
        staffs.fcm_token=token
        staffs.save()
        return HttpResponse("True")
    except: 
        return HttpResponse("False")  


def staff_all_notification(request):
    read = request.POST.get("notify")
    staffs=staff.objects.get(admin=request.user.id)
    notify = notificationstaff.objects.filter(staff_id=staffs.id,read=True).order_by("-id")
    notification = notificationstaff.objects.filter(staff_id=staffs.id,read=False).order_by("-id")
    notifications = notificationstaff.objects.filter(staff_id=staffs.id,read=False).count()
    paginator = Paginator(notify, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=3, on_ends=2)
    try:
        notify = paginator.page(page)
    except PageNotAnInteger:
        notify = paginator.page(1)
    except EmptyPage:
        notify = paginator.page(paginator.num_pages)
    return render(request,"staff_template/Notifications.html",{"notification":notification,"notify":notify,"notifications":notifications,
                                                               "page_range":page_range,
                                                               "page_obj":page_obj
                                                               })


def staff_add_result(request):
    subjects=subject.objects.filter(staff_id=request.user.id)
    session_years=sessionmodel.objects.all()
    staffs = staff.objects.get(admin=request.user.id)
    notifications = notificationstaff.objects.filter(staff_id=staffs.id,read=False).count()
    notification = notificationstaff.objects.filter(staff_id=staffs.id,read=False)

    return render(request,"staff_template/add_result.html",{"notification":notification,"subjects":subjects,"session_years":session_years,"notifications": notifications})

def result_save(request):
    if request.method!='POST':
        return HttpResponseRedirect("staff_add_result")
    student_admin_id=request.POST.get("student_list") 
    assignment_marks=request.POST.get("assignment") 
    exam_marks=request.POST.get("exam_marks")  
    subject_id=request.POST.get("subjects")

    student_obj=CustomUser.objects.get(id=student_admin_id)
    std=students.objects.get(admin=student_admin_id)
    subject_obj=subject.objects.get(id=subject_id)
    if assignment_marks!="" or exam_marks!="":
        grade = float(assignment_marks) + float(exam_marks)
    elif assignment_marks == "" or exam_marks == "":
        grade = 0
    Stage1 = semester.objects.get(id=19)
    print(grade)
    if grade >= 70:
        Grade = "A"
    elif grade >= 60:
        Grade = "B"
    elif grade >= 50:
        Grade = "C"
    elif grade >= 40:
        Grade = "D"
    elif grade > 0 and grade < 40:
        Grade = "E"
    elif grade <= 0:
        Grade = "X"
    try:
        check_exists=StudentResult.objects.filter(subject_id=subject_obj,student_id=student_obj).exists()
        if check_exists:
            result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
            if assignment_marks != "" or exam_marks != "":
                result.subject_exam_marks=exam_marks
                result.subject_assignment_marks=assignment_marks
            elif assignment_marks == "" or exam_marks == "":
                result.subject_exam_marks = 0
                result.subject_assignment_marks = 0
            if grade >= 70:
                result.grade = "A"
            elif grade >= 60:
                result.grade = "B"
            elif grade >= 50:
                result.grade = "C"
            elif grade >= 40:
                result.grade = "D"
            elif  grade > 0 and grade < 40:
                result.grade = "E"
            elif grade <= 0:
                result.grade="X"
            result.save()
            reg = registrationreport.objects.get(student_id=student_obj,subject_id=subject_obj)
            reg.status=0
            reg.save()
            reg1 = registrationreport.objects.filter(student_id=student_obj,status=1,semester_id=std.stage_id.id).count()
            reg2 = int(reg1)
            std1 = students.objects.get(admin=student_admin_id)
            if reg2 <= 0:
                std1.stage_id = Stage1
                std1.status = False
            std1.save()
            messages.success(request, "Results Updated")
            return HttpResponseRedirect(reverse("result_save"))
        else:
            result=StudentResult(grade=Grade, subject_assignment_marks=assignment_marks,subject_exam_marks=exam_marks,student_id=student_obj,subject_id=subject_obj,semester_id=subject_obj.stage_id)
            result.save()
            reg = registrationreport.objects.get(student_id=student_obj, subject_id=subject_obj)
            reg.status = 0
            reg.save()
            reg1 = registrationreport.objects.filter(student_id=student_obj, status=1, semester_id=std.stage_id.id).count()
            std1 = students.objects.get(admin=student_admin_id)
            reg2 = int(reg1)
            if reg2 <= 0:
                std1.stage_id = Stage1
                std1.status = False
            std1.save()
            messages.success(request, "Results Saved")
            return HttpResponseRedirect(reverse("result_save"))
    except:
        messages.error(request, "Failed To upload Results")
        return HttpResponseRedirect(reverse("result_save"))

@csrf_exempt
def fetch_student_result(request):
    subject_id=request.POST.get("subject_id")
    student_id=request.POST.get("student_id")
    student_obj=CustomUser.objects.get(id=student_id)
    result=StudentResult.objects.filter(subject_id=subject_id,student_id=student_obj.id).exists()
    if result:
        result=StudentResult.objects.get(subject_id=subject_id,student_id=student_obj.id)
        result_data={"exam_marks":result.subject_exam_marks,"assign_marks":result.subject_assignment_marks}
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")    


def start_live_classroom(request):
    subjects=subject.objects.filter(staff_id=request.user.id)
    session_years=sessionmodel.objects.all()
    return render(request,"staff_template/start_live_classroom.html",{"subjects":subjects,"session_years":session_years})


def start_live_classroom_process(request):
    session_year=request.POST.get("session_year")
    Subject=request.POST.get("Subject")

    subject_obj=subject.objects.get(id=Subject)
    session_obj=sessionmodel.objects.get(id=session_year)
    checks=OnlineClassRoom.objects.filter(subjects=subject_obj,session_years=session_obj,is_active=True).exists()
    if checks:
        data=OnlineClassRoom.objects.get(subjects=subject_obj,session_years=session_obj,is_active=True)
        room_pwd=data.room_pwd
        roomname=data.room_name
    else:
        room_pwd=datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        roomname=datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        staff_obj=staff.objects.get(admin=request.user.id)
        onlineClass=OnlineClassRoom(room_name=roomname,room_pwd=room_pwd,subjects=subject_obj,session_years=session_obj,started_by=staff_obj,is_active=True)
        onlineClass.save()
    context={
        "username":request.user.username,
        "password":room_pwd,
        "roomid":roomname,
        "subject":subject_obj.subject_name,
        "session_year":session_obj
    }
    return render(request,"staff_template/live_class_room_start.html",context)

def returnHtmlWidget(request):
    return render(request,"widget.html")


def read_save(request):
    staffs = staff.objects.get(admin=request.user.id)
    reg = request.POST.get("read")
    reg1 = request.POST.get("read1")
    read2 = True
    notification = notificationstaff.objects.filter(staff_id=staffs.id,read=False).exists()
    try:
        if notification:
            notification1 = notificationstaff.objects.get(staff_id=staffs.id,id=reg1)
            notification1.read=reg
            notification1.save()
        return HttpResponseRedirect(reverse("staff_all_notification"))
    except:
        return HttpResponseRedirect(reverse("staff_all_notification"))

def clear_all_staff(request):
    staffs = staff.objects.get(admin=request.user.id)
    notify1 = notificationstaff.objects.filter(staff_id=staffs.id,read=1)
    notify1.delete()
    return HttpResponseRedirect(reverse("staff_all_notification"))

def clear_one_staff(request):
    staff_id = request.POST.get("notification")
    notify1 = notificationstaff.objects.filter(id=staff_id,read=1)
    notify1.delete()
    return HttpResponseRedirect(reverse("staff_all_notification"))

def registered_units(request):
    session = sessionmodel.objects.all()
    reg = semester.objects.all()
    subjects = subject.objects.filter(staff_id=request.user.id)
    context = {
        "session":session,
        "reg":reg,
        "subjects":subjects
    }
    return render(request,"staff_template/units.html",context)


@csrf_exempt
def get_registered_units(request):
    stage_id = request.POST.get("stage")
    session_id = request.POST.get("session")
    subjects = request.POST.get("subjects")
    Hod = staff.objects.get(admin=request.user.id)
    reg1 = registrationreport.objects.filter(subject_id=subjects,semester_id=stage_id,dept_id=Hod.dept_id.id,session_id=session_id,status=True)
    list_data = []
    for Subject in reg1:
        data_small = {"id": Subject.id, "code": Subject.student_id.username, "name": Subject.student_id.first_name,"marks":Subject.subject_id.subject_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def unit_pdf_view(request):
    Stage = request.POST.get("stage")
    session = request.POST.get("session")
    subjects = request.POST.get("subjects")
    subject_id = subject.objects.get(id=subjects)
    session_id = sessionmodel.objects.get(id=session)
    Hod = staff.objects.get(admin=request.user.id)
    student = registrationreport.objects.filter(subject_id=subjects,dept_id=Hod.dept_id.id,status=1,semester_id=Stage,session_id=session)
    template_path = 'staff_template/registered_units.html'
    context = {'student': student,
               "Hod":Hod,
               "session":session_id,
               "subject_id":subject_id
               }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=''Registered_students-'+subject_id.code+'.pdf'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('we had some errors <pre>' + html + '</pre>')
    return response
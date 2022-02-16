#from django.contrib.core import serializers
from datetime import datetime
import json
from uuid import uuid4

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from Student.models import Adminhod, CustomUser, OnlineClassRoom, StudentResult, attendance, attendancereport, courses, leavereportstaff, notificationstaff, staff, subject, sessionmodel, students, \
    feedbackstaff
from django.contrib import messages

def staff_home(request):
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
    # print(Subjects.count())
    subject_count=Subjects.count()
    
    subject_list=[]
    attendance_list=[]
    for Subject in Subjects:
        Attendance_count1=attendance.objects.filter(subject_id=Subject.id).count()
        subject_list.append(Subject.subject_name)
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
    return render(request,"staff_template/staff_home_template.html",{"student_count":student_count,"Attendance_count":Attendance_count,"leave_count":leave_count,"subject_count":subject_count,"subject_list":subject_list,"attendance_list":attendance_list,"student_list":student_list,"present_list":student_list_attendance_present,"absent_list":student_list_attendance_absent})

def staff_take_attendance(request):
    subjects = subject.objects.filter(staff_id=request.user.id)
    session_years = sessionmodel.objects.all()
    return render(request,"staff_template/staff_take_attendance.html",{"subjects":subjects,"session_years":session_years})

@csrf_exempt
def get_students(request):
    subject_id=request.POST.get("subjects")
    session_year = request.POST.get("session_year")

    Subject = subject.objects.get(id=subject_id)
    session_model = sessionmodel.objects.get(id=session_year)
    student = students.objects.filter(course_id=Subject.course_id,session_year_id=session_model)
    list_data = []
    for student in student:
        data_small = {"id":student.admin.id,"name":student.admin.first_name+"  "+student.admin.last_name}
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
            attendance_report=attendancereport(student_id=student,attendance_id=Attendance,status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_update_attendance(request):
    subjects = subject.objects.filter(staff_id=request.user.id)
    session_year_id = sessionmodel.objects.all()
    return render(request,"staff_template/update_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})         

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
        data_small = {"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+"  "+student.student_id.admin.last_name,"status":student.status}
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
    leave_data=leavereportstaff.objects.filter(staff_id=staff_obj)
    return render(request,"staff_template/staff_apply_leave.html",{"leave_data":leave_data})


def staff_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")  
        leave_msg=request.POST.get("leave_msg")
        staff_obj = staff.objects.get(admin=request.user.id)
        try:
            leave_report=leavereportstaff(staff_id=staff_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request,"Successfully Applied For Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
             messages.error(request, "Failed To Apply For Leave")
             return HttpResponseRedirect(reverse("staff_apply_leave"))




def staff_feedback(request):
    staff_obj = staff.objects.get(admin=request.user.id)
    feedback_data = feedbackstaff.objects.filter(staff_id=staff_obj)
    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data})


def staff_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_feedback"))
    else:
        feedback_msg = request.POST.get("feedback_msg")
        staff_obj = staff.objects.get(admin=request.user.id)
        try:
            feedback_obj = feedbackstaff(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
            feedback_obj.save()
            messages.success(request, "Successfully Submitted Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Failed To Submit Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))

def staff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    staffs=staff.objects.get(admin = user)
    return render(request,"staff_template/staff_profile.html",{"user":user,"staffs":staffs})  


def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:    
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
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
    staffs=staff.objects.get(admin=request.user.id)
    notification=notificationstaff.objects.filter(staff_id=staffs.id)
    return render(request,"staff_template/Notifications.html",{"notification":notification})        


def staff_add_result(request):
    subjects=subject.objects.filter(staff_id=request.user.id)
    session_years=sessionmodel.objects.all()
    return render(request,"staff_template/add_result.html",{"subjects":subjects,"session_years":session_years})

def result_save(request):
    if request.method!='POST':
        return HttpResponseRedirect("staff_add_result")
    student_admin_id=request.POST.get("student_list") 
    assignment_marks=request.POST.get("assignment") 
    exam_marks=request.POST.get("exam_marks")  
    subject_id=request.POST.get("subjects")

    student_obj=students.objects.get(admin=student_admin_id)
    subject_obj=subject.objects.get(id=subject_id)
    try:
        check_exists=StudentResult.objects.filter(subject_id=subject_obj,student_id=student_obj).exists()
        if check_exists:
            result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
            result.subject_exam_marks=exam_marks
            result.subject_assignment_marks=assignment_marks
            result.save()
            messages.success(request, "Results Updated")
            return HttpResponseRedirect(reverse("result_save"))
        else:    
            result=StudentResult(subject_assignment_marks=assignment_marks,subject_exam_marks=exam_marks,student_id=student_obj,subject_id=subject_obj)
            result.save()
            messages.success(request, "Results Saved")
            return HttpResponseRedirect(reverse("result_save"))
    except:
        messages.error(request, " Failed To upload Results")
        return HttpResponseRedirect(reverse("result_save")) 

@csrf_exempt
def fetch_student_result(request):
    subject_id=request.POST.get("subject_id")
    student_id=request.POST.get("student_id")
    student_obj=students.objects.get(admin=student_id)
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
    subjects=request.POST.get("subject")

    subject_obj=subject.objects.get(id=subjects)
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

    return render(request,"staff_template/live_class_room_start.html",{"username":request.user.username,"password":room_pwd,"roomid":roomname,"subject":subject_obj.subject_name,"session_year":session_obj})

def returnHtmlWidget(request):
    return render(request,"widget.html")

import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt



from Student.models import OnlineClassRoom, StudentResult, feedbackstudent, leavereportstudent, notificationstudent, sessionmodel, students, courses, subject, CustomUser, attendance, attendancereport


def student_home(request):
    student_obj=students.objects.get(admin=request.user.id)
    Attendance_total=attendancereport.objects.filter(student_id=student_obj).count()
    Attendance_present=attendancereport.objects.filter(student_id=student_obj,status=True).count()
    Attendance_absent=attendancereport.objects.filter(student_id=student_obj,status=False).count()
    course=courses.objects.get(id=student_obj.course_id.id)
    subjects=subject.objects.filter(course_id=course).count()
    # pic=students.objects.get("profile_pic")
    # subjects_data=subject.objects.filter(course_id=course)
    # session_obj=sessionmodel.objects.get(id=student_obj.session_year_id.id)
    # class_room=OnlineClassRoom.objects.filter(subjects__in=subjects_data,is_active=True,session_years=session_obj)
    subject_name=[]
    data_present=[]
    data_absent=[]
    subject_data=subject.objects.filter(course_id=student_obj.course_id)
    for Subjects in subject_data:
        Attendance=attendance.objects.filter(subject_id=Subjects.id)
        Attendance_present_count=attendancereport.objects.filter(attendance_id__in=Attendance,status=True,student_id=student_obj.id).count()
        Attendance_absent_count=attendancereport.objects.filter(attendance_id__in=Attendance,status=False,student_id=student_obj.id).count()
        subject_name.append(Subjects.subject_name)
        data_present.append(Attendance_present_count)
        data_absent.append(Attendance_absent_count)


    return render(request,"student_template/student_home_template.html",{"Attendance_total":Attendance_total,"Attendance_present":Attendance_present,"Attendance_absent":Attendance_absent,"subjects":subjects,"data_name":subject_name,"data1":data_present,"data2":data_absent})

# def join_class_room(request,subject_id,session_year_id):
#     session_year_obj=sessionmodel.object.get(id=session_year_id)
#     subjects=subject.objects.filter(id=subject_id)
#     if subjects.exists():
#         session=sessionmodel.object.filter(id=session_year_obj.id)
#         if session.exists():
#             subject_obj=subject.objects.get(id=subject_id)
#             course=courses.objects.get(id=subject_obj.course_id.id)
#             check_course=students.objects.filter(admin=request.user.id,course_id=course.id)
#             if check_course.exists():
#                 session_check=students.objects.filter(admin=request.user.id,session_year_id=session_year_obj.id)
#                 if session_check.exists():
#                     onlineclass=OnlineClassRoom.objects.get(session_years=session_year_id,subject=subject_id)
#                     return render(request,"student_template/join_class_room_start.html",{"username":request.user.username,"password":onlineclass.room_pwd,"roomid":onlineclass.room_name})

#                 else:
#                     return HttpResponse("This Online Session is Not For You")
#             else:
#                 return HttpResponse("This Subject is Not For You")
#         else:
#             return HttpResponse("Session Year Not Found")
#     else:
#         return HttpResponse("Subject Not Found")


def student_view_attendance(request):
    student=students.objects.get(admin=request.user.id)
    course=student.course_id
    subjects=subject.objects.filter(course_id=course)
    return render(request,"student_template/my_attendance.html",{"subjects":subjects})

def student_view_attendance_save(request):
    subject_id=request.POST.get("subjects")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj=subject.objects.get(id=subject_id)
    user_object=CustomUser.objects.get(id=request.user.id)
    stud_obj=students.objects.get(admin=user_object)

    Attendance=attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
    attendance_reports=attendancereport.objects.filter(attendance_id__in=Attendance,student_id=stud_obj)
    return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})

def student_apply_leave(request):
    student_obj = students.objects.get(admin=request.user.id)
    leave_data=leavereportstudent.objects.filter(student_id=student_obj)
    return render(request,"student_template/student_apply_leave.html",{"leave_data":leave_data})


def student_apply_leave_save(request):
    pass
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")  
        leave_msg=request.POST.get("leave_msg")
        student_obj = students.objects.get(admin=request.user.id)
        try:
            leave_report=leavereportstudent(student_id=student_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request,"Successfully Applied For Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
             messages.error(request, "Failed To Apply For Leave")
             return HttpResponseRedirect(reverse("student_apply_leave"))




def student_feedback(request):
    student_obj = students.objects.get(admin=request.user.id)
    feedback_data = feedbackstudent.objects.filter(student_id=student_obj)
    return render(request,"student_template/student_feedback.html",{"feedback_data":feedback_data})


def student_feedback_save(request):
   if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback"))
   else:
        feedback_msg = request.POST.get("feedback_msg")
        student_obj = students.objects.get(admin=request.user.id)
        try:
            feedback_obj = feedbackstudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="")
            feedback_obj.save()
            messages.success(request, "Successfully Submitted Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed To Submit Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))


def student_profile(request):
    User=CustomUser.objects.get(id=request.user.id)
    student=students.objects.get(admin=User)
    return render(request,"student_template/student_profile.html",{"User":User,"student":student})  

def student_profile_save(request):
    first_name=request.POST.get("first_name") 
    last_name=request.POST.get("last_name") 
    password=request.POST.get("password")
    address=request.POST.get("address")
    
    customuser=CustomUser.objects.get(id=request.user.id)
    try:
        customuser.first_name=first_name
        customuser.last_name=last_name
        customuser.save()
        student=students.objects.get(admin=customuser)
        student.address=address
        student.save()
        if password!=None and password!="":
            customuser.set_password(password)
        messages.success(request,"Profile Changed")
        return HttpResponseRedirect(reverse("student_profile"))
    except:
        messages.error(request, "Profile not changed")
        return HttpResponseRedirect(reverse("student_profile")) 


@csrf_exempt
def student_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        student=students.objects.get(admin=request.user.id)
        student.fcm_token=token
        student.save()
        return HttpResponse("True")
    except: 
        return HttpResponse("False") 

def showFirebaseJS(request):
    pass

def student_all_notification(request):
    student=students.objects.get(admin=request.user.id)
    notification=notificationstudent.objects.filter(student_id=student.id)
    return render(request,"student_template/Notifications.html",{"notification":notification}) 


def student_view_result(request):
    student=students.objects.get(admin=request.user.id)
    studentresult=StudentResult.objects.filter(student_id=student.id)
    return render(request,"student_template/results.html",{"studentresult":studentresult})

def unit_registration(request):
    return render(request,"student_template/register_units.html")
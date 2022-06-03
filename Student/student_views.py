import datetime
import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.views.generic import ListView


from Student.models import OnlineClassRoom, StudentResult, feedbackstudent, leavereportstudent, notificationstudent, \
    sessionmodel, students, courses, subject, CustomUser, attendance, attendancereport, semester, unitregistration, \
    registrationreport


def student_home(request):
    student_obj=students.objects.get(admin=request.user.id)
    Attendance_total=attendancereport.objects.filter(student_id=student_obj).count()
    Attendance_present=attendancereport.objects.filter(student_id=student_obj,status=True).count()
    Attendance_absent=attendancereport.objects.filter(student_id=student_obj,status=False).count()
    course=courses.objects.get(id=student_obj.course_id.id)
    subjects=registrationreport.objects.filter(student_id=request.user.id,status=1).count()
    subjects_data=subject.objects.filter(course_id=course)
    session_obj=sessionmodel.objects.get(id=student_obj.session_year_id.id)
    class_room=OnlineClassRoom.objects.filter(subjects__in=subjects_data,is_active=True,session_years=session_obj)
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

    context={
        "Attendance_total":Attendance_total,
        "Attendance_present":Attendance_present,
        "Attendance_absent":Attendance_absent,
        "subjects":subjects,
        "data_name":subject_name,
        "data1":data_present,
        "data2":data_absent,
        "class_room":class_room
    }

    return render(request,"student_template/student_home_template.html",context)

def join_class_room(request,subject_id,session_year_id):
    session_year_obj=sessionmodel.objects.get(id=session_year_id)
    subjects=subject.objects.filter(id=subject_id)
    if subjects.exists():
        session=sessionmodel.objects.filter(id=session_year_obj.id)
        if session.exists():
            subject_obj=subject.objects.get(id=subject_id)
            course=courses.objects.get(id=subject_obj.course_id.id)
            check_course=students.objects.filter(admin=request.user.id,course_id=course.id)
            if check_course.exists():
                session_check=students.objects.filter(admin=request.user.id,session_year_id=session_year_obj.id)
                if session_check.exists():
                    onlineclass=OnlineClassRoom.objects.get(session_years=session_year_id,subjects=subject_id)
                    return render(request,"student_template/join_class_room_start.html",{"username":request.user.username,"password":onlineclass.room_pwd,"roomid":onlineclass.room_name})

                else:
                    return HttpResponse("This Online Session is Not For You")
            else:
                return HttpResponse("This Subject is Not For You")
        else:
            return HttpResponse("Session Year Not Found")
    else:
        return HttpResponse("Subject Not Found")


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
    user = CustomUser.objects.get(id=request.user.id)
    student = students.objects.get(admin=user)
    return render(request,"student_template/student_profile.html",{"student":student})

def student_profile_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        address = request.POST.get("address")
        password = request.POST.get("password")
        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None


        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            student = students.objects.get(admin=customuser)
            student.address = address
            if profile_pic_url != None:
                student.profile_pic = profile_pic_url
            student.save()
            if password != None and password != "":
                customuser.set_password(password)
            messages.success(request, "Profile Changed")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, " Failed To Change Profile ")
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


def student_all_notification(request):
    student=students.objects.get(admin=request.user.id)
    notification=notificationstudent.objects.filter(student_id=student.id)
    return render(request,"student_template/Notifications.html",{"notification":notification}) 


def student_view_result(request):
    student_obj = students.objects.get(admin=request.user.id)
    subject_data = subject.objects.filter(course_id=student_obj.course_id)
    Stage = semester.objects.all()
    reg = unitregistration.objects.filter(student_id=request.user.id)
    context = {
        "Stage": Stage,
        "student_obj": student_obj,
        "subject_data": subject_data,
        "reg": reg
    }
    return render(request, "student_template/results.html", context)

@csrf_exempt
def get_results(request):
    stage_id = request.POST.get("stage")
    student_obj = students.objects.get(admin=request.user.id)
    reg = StudentResult.objects.filter(student_id=student_obj,semester_id=stage_id)
    list_data = []
    for Subject in reg:
        check_exist = registrationreport.objects.filter(status=1, student_id=request.user.id, semester_id=stage_id,subject_id=Subject.subject_id).exists()
        if check_exist:
            Sum = int(Subject.subject_exam_marks) + int(Subject.subject_assignment_marks)
            data_small = {"id": Subject.id, "code": Subject.subject_id.code, "name": Subject.subject_id.subject_name,'marks':Sum}
            list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def Units(request):
    student_obj = students.objects.get(admin=request.user.id)
    subject_data = subject.objects.filter(course_id=student_obj.course_id)
    Stage = semester.objects.all()
    reg = unitregistration.objects.filter(student_id=request.user.id)
    context = {
        "Stage":Stage,
        "student_obj":student_obj,
        "subject_data":subject_data,
        "reg":reg
    }
    return render(request,"student_template/units.html", context)

@csrf_exempt
def units(request):
    stage_id = request.POST.get("stage")
    student_obj = students.objects.get(admin=request.user.id)
    subjects = subject.objects.filter(course_id=student_obj.course_id, stage_id=stage_id)
    reg = registrationreport.objects.filter(student_id=request.user.id, semester_id=stage_id,status=1)
    list_data = []
    for Subject in reg:
        data_small = {"id": Subject.id,"code": Subject.subject_id.code, "name": Subject.subject_id.subject_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def unit_registration(request):
    student_obj = students.objects.get(admin=request.user.id)
    subject_data = subject.objects.filter(course_id=student_obj.course_id)
    Stage = semester.objects.all()
    context = {
        "Stage":Stage,
        "student_obj":student_obj,
        "subject_data":subject_data,
    }
    return render(request,"student_template/unit_registration.html", context)

@csrf_exempt
def get_units(request):
    stage_id=request.POST.get("stage")
    student_obj = students.objects.get(admin=request.user.id)
    Subject = subject.objects.filter(course_id=student_obj.course_id,stage_id=stage_id)
    reg = unitregistration.objects.filter(student_id=request.user.id, semester_id=stage_id)
    list_data = []
    if reg.exists():
        return HttpResponse("Exists")
    for Subject in Subject:
        data_small = {"id": Subject.id,"code": Subject.code, "name": Subject.subject_name + ""}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


@csrf_exempt
def save_units_data(request):
    student_ids=request.POST.get("student_ids")
    stage_id=request.POST.get("stage_id")
    student_id=request.POST.get("student_id")
    stage_model = semester.objects.get(id=stage_id)
    Student = CustomUser.objects.get(id=student_id)
    json_student = json.loads(student_ids)
    try:
        Attendance=unitregistration(semester_id=stage_model,student_id=Student)
        Attendance.save()
        for stud in json_student:
            subjects = subject.objects.get(id=stud['id'])
            attendance_report=registrationreport(subject_id=subjects,student_id=Student,unit_id=Attendance,status=stud['status'],semester_id=stage_model)
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def deregister(request,id):
    if request.method == "POST":
        register=registrationreport(status=0)
        register.save()
        return HttpResponseRedirect(reverse('Units'))
    return render(request, "student_template/deregister.html")

def resit(request):
    reg = unitregistration.objects.filter(student_id=request.user.id)
    return render(request,"student_template/update_registration.html",{"reg":reg})

@csrf_exempt
def get_unregistered_units(request):
    stage=request.POST.get("stage")
    stage_id = unitregistration.objects.get(id=stage)
    attendance_data = registrationreport.objects.filter(student_id=request.user.id,unit_id=stage_id)
    list_data = []
    for student in attendance_data:
        data_small = {"id": student.subject_id.id,
                      "name": student.subject_id.subject_name,
                      "code":student.subject_id.code,
                      "status": student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def save_update_units(request):
    student_ids = request.POST.get("student_ids")
    stage = request.POST.get("stage")
    stage_id = unitregistration.objects.get(id=stage)
    json_student = json.loads(student_ids)
    try:
        for stud in json_student:
            student = CustomUser.objects.get(id=request.user.id)
            Subject = subject.objects.get(id=stud['id'])
            attendance_report = registrationreport.objects.get(student_id=student,unit_id=stage_id,subject_id=Subject)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

@csrf_exempt
def Result_List_View(request, **kwargs):
    Student = students.objects.get(admin=request.user.id)
    Subject = subject.objects.filter(course_id=Student.course_id)
    Obj = StudentResult.objects.filter(student_id=Student)
    return render(request,'student_template/main.html',{"Obj":Obj})


@csrf_exempt
def render_pdf(request, *args, **kwargs):
    # subject_id=kwargs.get('subject_id')
    # student_id = kwargs.get('student_id')
    # result = get_object_or_404(StudentResult)
    template_path = 'student_template/result.html'
    context = {'result': "result"}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('we had some errors <pre>' + html + '</pre>')
    return response
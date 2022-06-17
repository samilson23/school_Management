from audioop import reverse
from os import rename
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from Student.forms import EditResultForm
from Student.models import StudentResult, students, subject, CustomUser, staff, notificationstaff
from django.contrib import messages

class EditResultViewClass(View):
    def get(self,request,*args,**kwargs):
        staff_id=request.user.id
        Edit_result_form=EditResultForm(staff_id=staff_id)
        staff_obj = staff.objects.get(admin=request.user.id)
        notifications = notificationstaff.objects.filter(staff_id=staff_obj.id,read=False).count()
        notification = notificationstaff.objects.filter(staff_id=staff_obj.id,read=False)
        return render(request,"staff_template/edit_student_result.html",{"notification":notification,"form":Edit_result_form,"notifications":notifications})

    def post(self,request,*args,**kwargs):
        form=EditResultForm(request.POST,staff_id=request.user.id)
        if form.is_valid():
            student_admin_id=form.cleaned_data["student_ids"]
            assignment_marks=form.cleaned_data["assignment_marks"] 
            exam_marks=form.cleaned_data["exam_marks"]
            subject_id=form.cleaned_data["subject_id"]
            grade = float(assignment_marks) + float(exam_marks)
            print(grade)
            if grade >= 70:
                Grade = "A"
            elif grade >= 60:
                Grade = "B"
            elif grade >= 50:
                Grade = "C"
            elif grade >= 40:
                Grade = "D"
            elif grade < 40:
                Grade = "E"

            student_obj=CustomUser.objects.get(id=student_admin_id)
            subject_obj=subject.objects.get(id=subject_id) 
            result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
            result.subject_exam_marks=exam_marks
            result.subject_assignment_marks=assignment_marks
            result.grade=Grade
            result.save()
            messages.success(request, "Results Successfully changed")
            return HttpResponseRedirect("/edit_student_result")
        else:
            messages.error(request, "Results Not Updated")
            form=EditResultForm(request.POST,staff_id=request.user.id)
            return render(request,"staff_template/edit_student_result.html",{"form":form})
            


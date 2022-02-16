from audioop import reverse
from os import rename
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from Student.forms import EditResultForm
from Student.models import StudentResult, students, subject
from django.contrib import messages

class EditResultViewClass(View):
    def get(self,request,*args,**kwargs):
        staff_id=request.user.id
        Edit_result_form=EditResultForm(staff_id=staff_id)
        return render(request,"staff_template/edit_student_result.html",{"form":Edit_result_form})

    def post(self,request,*args,**kwargs):
        form=EditResultForm(request.POST,staff_id=request.user.id)
        if form.is_valid():
            student_admin_id=form.cleaned_data["student_ids"] 
            assignment_marks=form.cleaned_data["assignment_marks"] 
            exam_marks=form.cleaned_data["exam_marks"]
            subject_id=form.cleaned_data["subject_id"]

            student_obj=students.objects.get(admin=student_admin_id)
            subject_obj=subject.objects.get(id=subject_id) 
            result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
            result.subject_exam_marks=exam_marks
            result.subject_assignment_marks=assignment_marks
            result.save()
            messages.success(request, "Results Successfully changed")
            return HttpResponseRedirect("/edit_student_result")
        else:
            messages.error(request, "Results Not Updated")
            form=EditResultForm(request.POST,staff_id=request.user.id)
            return render(request,"staff_template/edit_student_result.html",{"form":form})
            


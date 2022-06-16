
from random import choices
from django import forms
from django.forms import ChoiceField, PasswordInput, EmailInput, TextInput

from Student.models import courses, students, sessionmodel, subject


class DateInput(forms.DateInput):
    input_type = "date"


class ChoiceNoValidation(ChoiceField):
    def validate(self,value):
        pass

# class AddstudentForm(forms.Form):
#
#     email = forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
#     password = forms.CharField(label="Password", max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
#     first_name = forms.CharField(label="Firstname", max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
#     last_name = forms.CharField(label="Lastname", max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
#     username = forms.CharField(label="Username", max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
#     address = forms.CharField(label="Address", max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
#     course_list = []
#     try:
#         course = courses.objects.all()
#         for course in course:
#             small_course = (course.id, course.course_name)
#             course_list.append(small_course)
#     except:
#         course_list = []
#     course = forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
#     session_list = []
#     try:
#         sessions = sessionmodel.objects.all()
#         for ses in sessions:
#             small_ses = (ses.id, str(ses.session_start_year)+"  TO  "+str(ses.session_end_year))
#             session_list.append(small_ses)
#     except:
#         session_list = []
#
#     gender_choice = (
#         ('Male',"Male"),
#         ('Female',"Female")
#     )
#
#     sex = forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
#     session_year_id = forms.ChoiceField(label="Session Year",widget=forms.Select(attrs={"class":"form-control"}),choices=session_list)
#     profile_pic = forms.FileField(label="Profile Pic", max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))

class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email/Phone", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control","autocomplete":"off"}))
    first_name = forms.CharField(label="Firstname", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Lastname", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control","autocomplete":"off"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    course_list=[]
    try:
        course = courses.objects.all()
        for course in course:
            small_course = (course.id, course.course_name)
            course_list.append(small_course)
    except:        
        course_list = []

    session_list = []
    try:
        sessions = sessionmodel.objects.all()
        for ses in sessions:
            small_ses = (ses.id, str(ses.session_start_year)+"  TO  "+str(ses.session_end_year))
            session_list.append(small_ses)
    except:    
        session_list = []

    gender_choice = (
        ('Male',"Male"),
        ('Female',"Female")
    )
    course = forms.ChoiceField(label="Course", choices=course_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", widget=forms.Select(attrs={"class": "form-control"}),choices=session_list)
    profile_pic = forms.FileField(label="Profile Pic", max_length=50,
                                  widget=forms.FileInput(attrs={"class": "form-control"}), required=False)


class EditResultForm(forms.Form):
    def __init__(self,*args, **kwargs):
        self.staff_id=kwargs.pop("staff_id")
        super(EditResultForm,self).__init__(*args,**kwargs)

        subject_list=[]
        try:
            subjects=subject.objects.filter(staff_id=self.staff_id)
            for Subject in subjects:
                subjects_single=(Subject.id,Subject.code)
                subject_list.append(subjects_single)
        except:
            subject_list=[] 
        self.fields['subject_id'].choices=subject_list

    session_list=[]
    try:
        sessions=sessionmodel.objects.all()
        for session in sessions:
            session_single=(session.id,str(session.session_start_year)+" TO "+str(session.session_end_year))
            session_list.append(session_single)
    except:
        session_list=[]        

    subject_id=forms.ChoiceField(label="Subject",widget=forms.Select(attrs={"class":"form-control"}))       
    session_ids=forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    student_ids=ChoiceNoValidation(label="Student",widget=forms.Select(attrs={"class":"form-control"})) 
    assignment_marks=forms.CharField(label="Assignment Marks",widget=forms.TextInput(attrs={"class":"form-control"})) 
    exam_marks=forms.CharField(label="Exam Marks",widget=forms.TextInput(attrs={"class":"form-control"}))


class EditProfile(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control","autocomplete":"off","disabled":"disabled"}),required=False)
    first_name = forms.CharField(label="Firstname", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control","disabled":"disabled"}),required=False)
    last_name = forms.CharField(label="Lastname", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control","disabled":"disabled"}),required=False)
    username = forms.CharField(label="Username", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control","autocomplete":"off","disabled":"disabled"}),required=False)
    password = forms.CharField(label="Id Number", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off","placeholder":"Only Fill if you want to change your password"}),required=False)
    profile_pic = forms.FileField(label="Profile Pic", max_length=50,
                                  widget=forms.FileInput(attrs={"class": "form-control"}), required=False)

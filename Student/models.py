from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

class sessionmodel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()

class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(3,"staff"),(4,"student"),(2,"admin"))
    user_type= models.CharField(default=1, choices=user_type_data,max_length=10)

class school(models.Model):
    id=models.AutoField(primary_key=True)
    school_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class department(models.Model):
    id=models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)
    school_id = models.ForeignKey(school, on_delete=models.CASCADE,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Adminhod(models.Model):
   id = models.AutoField(primary_key=True)
   admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now_add=True)
   objects=models.Manager()


class hod(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(department, on_delete=models.CASCADE,default=1)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # fcm_token=models.TextField(default="")
    objects=models.Manager()

class semester(models.Model):
    id = models.AutoField(primary_key=True)
    stage = models.CharField(max_length=250,default=1.1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=250)
    dept_id = models.ForeignKey(department,on_delete=models.CASCADE,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    dept_id = models.ForeignKey(department, on_delete=models.SET_DEFAULT, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()

class subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=250)
    code = models.CharField(max_length=250)
    course_id = models.ForeignKey(courses,on_delete=models.SET_DEFAULT,default=1)
    stage_id = models.ForeignKey(semester,on_delete=models.SET_DEFAULT,default=1)
    dept_id = models.ForeignKey(department, on_delete=models.SET_DEFAULT, default=1)
    staff_id = models.ForeignKey(CustomUser,on_delete=models.SET_DEFAULT,default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class students(models.Model):
    id=models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id=models.ForeignKey(courses,on_delete=models.SET_DEFAULT,default=1)
    dept_id = models.ForeignKey(department,on_delete=models.SET_DEFAULT,default=1)
    session_year_id = models.ForeignKey(sessionmodel,on_delete=models.CASCADE)
    stage_id = models.ForeignKey(semester,on_delete=models.SET_DEFAULT,default=19)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()

class attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(subject, on_delete=models.CASCADE)
    attendance_date = models.DateField(auto_now_add=False)
    session_year_id = models.ForeignKey(sessionmodel, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager()

class unitregistration(models.Model):
    id = models.AutoField(primary_key=True)
    semester_id = models.ForeignKey(semester,on_delete=models.CASCADE)
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=6)
    session_id = models.ForeignKey(sessionmodel, on_delete=models.CASCADE,default=1)
    dept_id = models.ForeignKey(department, on_delete=models.CASCADE,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class registrationreport(models.Model):
    id = models.AutoField(primary_key=True)
    unit_id = models.ForeignKey(unitregistration, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(subject, on_delete=models.CASCADE)
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=6)
    semester_id = models.ForeignKey(semester, on_delete=models.CASCADE)
    session_id = models.ForeignKey(sessionmodel, on_delete=models.CASCADE, default=1)
    dept_id = models.ForeignKey(department, on_delete=models.CASCADE, default=1)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class attendancereport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(students, on_delete=models.CASCADE)
    attendance_id = models.ForeignKey(attendance, on_delete=models.CASCADE)
    stage_id = models.ForeignKey(semester,on_delete=models.CASCADE,default=19)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager() 


class leavereportstudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id=models.ForeignKey(students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=50)
    leave_message = models.CharField(max_length=50)
    dept_id = models.ForeignKey(department, on_delete=models.SET_DEFAULT, default=1)
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager() 

class leavereportstaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(staff, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=50)
    leave_message = models.CharField(max_length=50)
    dept_id = models.ForeignKey(department, on_delete=models.SET_DEFAULT, default=1)
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager() 


class feedbackstudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id=models.ForeignKey(students, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(department, on_delete=models.CASCADE)
    status = models.BooleanField(default=0)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager() 


class feedbackstaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(staff, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(department, on_delete=models.CASCADE)
    status = models.BooleanField(default=0)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager() 

class notificationstudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id=models.ForeignKey(students, on_delete=models.CASCADE)
    Hod_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=3)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager()  

class notificationstaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(staff, on_delete=models.CASCADE)
    message = models.TextField()
    Hod_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=3)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager()    


class StudentResult(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    subject_id=models.ForeignKey(subject,on_delete=models.CASCADE)
    semester_id=models.ForeignKey(semester,on_delete=models.CASCADE)
    subject_exam_marks=models.FloatField(default=0)
    subject_assignment_marks=models.FloatField(default=0)
    grade = models.CharField(max_length=100)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    objects=models.Manager()

class OnlineClassRoom(models.Model):
    id=models.AutoField(primary_key=True)
    room_name=models.CharField(max_length=255)
    room_pwd=models.CharField(max_length=255)
    subjects=models.ForeignKey(subject,on_delete=models.CASCADE)
    session_years=models.ForeignKey(sessionmodel,on_delete=models.CASCADE)
    started_by=models.ForeignKey(staff,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()      

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        if instance.user_type==1:
            Adminhod.objects.create(admin=instance)
    if created:
        if instance.user_type==2:
            hod.objects.create(admin=instance)

    if created:
        if instance.user_type==3:
            staff.objects.create(admin=instance)

    if created:
        if instance.user_type==4:
            students.objects.create(admin=instance,course_id=courses.objects.get(id=1),session_year_id=sessionmodel.objects.get(id=1),address="",profile_pic="",gender="")

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender,instance, **kwargs):
    if instance.user_type==1:
        instance.adminhod.save()

    if instance.user_type==2:
        instance.hod.save()

    if instance.user_type==3:
        instance.staff.save()

    if instance.user_type==4:
        instance.students.save()             
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



class Adminhod(models.Model):
   id = models.AutoField(primary_key=True)
   admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now_add=True)
   objects=models.Manager()


class hod(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # fcm_token=models.TextField(default="")
    objects=models.Manager()


class staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()

class courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()    

# class semesters(models.Model):
#     id=models.AutoField(primary_key=True)
#     stage=models.ChoiceField(max_length=200)
#     course_id = models.ForeignKey(courses, on_delete=models.CASCADE, default=1)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()

class subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=250)
    course_id = models.ForeignKey(courses,on_delete=models.CASCADE,default=1)
    stage=models.CharField(max_length=100,default=1)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class students(models.Model):
    id=models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id=models.ForeignKey(courses,on_delete=models.DO_NOTHING,default=1)
    session_year_id = models.ForeignKey(sessionmodel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()

class attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(subject, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField(auto_now_add=False)
    session_year_id = models.ForeignKey(sessionmodel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager()  

class attendancereport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager() 

class leavereportstudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id=models.ForeignKey(students, on_delete=models.DO_NOTHING)
    leave_date = models.CharField(max_length=50)
    leave_message = models.CharField(max_length=50)
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager() 

class leavereportstaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(staff, on_delete=models.DO_NOTHING)
    leave_date = models.CharField(max_length=50)
    leave_message = models.CharField(max_length=50)
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager() 


class feedbackstudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id=models.ForeignKey(students, on_delete=models.DO_NOTHING)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager() 


class feedbackstaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(staff, on_delete=models.DO_NOTHING)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager() 

class notificationstudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id=models.ForeignKey(students, on_delete=models.DO_NOTHING)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager()  

class notificationstaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(staff, on_delete=models.DO_NOTHING)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=models.Manager()    


class StudentResult(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(students,on_delete=models.CASCADE)
    subject_id=models.ForeignKey(subject,on_delete=models.CASCADE)
    subject_exam_marks=models.FloatField(default=0)
    subject_assignment_marks=models.FloatField(default=0)
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
    is_active=models.BooleanField(default=True)
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
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from Student.models import CustomUser

# Register your models here.

class usermodel(UserAdmin):
    pass

admin.site.register(CustomUser,usermodel)

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        print(modulename)
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "Student.admin_views":
                    pass
                elif modulename == "Student.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("home"))

            elif user.user_type == "2":
                if modulename == "Student.hod_views":
                    pass
                elif modulename == "Student.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "3":
                if modulename == "Student.staffviews" or modulename == "Student.EditResultVIewClass":
                    pass
                elif modulename == "Student.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "4":
                if modulename == "Student.student_views" or modulename == "django.views.static":
                    pass
                elif modulename == "Student.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("dologin") or modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites" or modulename=="Student.views":
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))
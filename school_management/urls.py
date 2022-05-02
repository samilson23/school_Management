"""school_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/',



"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from Student import views, hod_views, staffviews, student_views, admin_views
from Student.EditResultViewClass import EditResultViewClass
from school_management import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("home",views.home),
    path('accounts/',include("django.contrib.auth.urls")),
    path('',views.showLoginPage,name="show_login"),
    path('doLogin',views.doLogin,name="dologin"),
    path('get_user_details',views.GetUserDetails,name="get_user_details"),
    path('logout_user',views.logout_user,name="logout_user"),
    path('admin_home',hod_views.admin_home,name="admin_home"),
    path('add_staff',hod_views.add_staff,name="add_staff"),
    path('add_staff_save',hod_views.add_staff_save,name="add_staff_save"),
    path('add_course', hod_views.add_course,name="add_course"),
    path('add_course_save', hod_views.add_course_save,name="add_course_save"),
    path('add_student', hod_views.add_student,name="add_student"),
    path('add_student_save', hod_views.add_student_save,name="add_student_save"),
    path('add_subject', hod_views.add_subject,name="add_subject"),
    path('add_subject_save', hod_views.add_subject_save,name="add_subject_save"),
    path('manage_staff', hod_views.manage_staff,name="manage_staff"),
    path('manage_student', hod_views.manage_student,name="manage_student"),
    path('manage_course', hod_views.manage_course,name="manage_course"),
    path('manage_subjects', hod_views.manage_subjects,name="manage_subjects"),
    path('edit_staff/<str:staff_id>', hod_views.edit_staff,name="edit_staff"),
    path('edit_staff_save', hod_views.edit_staff_save,name="edit_staff_save"),
    path('edit_student/<str:student_id>', hod_views.edit_student,name="edit_student"),
    path('edit_student_save', hod_views.edit_student_save,name="edit_student_save"),
    path('edit_subject/<str:subject_id>', hod_views.edit_subject,name="edit_subject"),
    path('edit_subject_save', hod_views.edit_subject_save,name="edit_subject_save"),
    path('edit_course/<str:course_id>', hod_views.edit_course,name="edit_course"),
    path('edit_course_save', hod_views.edit_course_save,name="edit_course_save"),
    path('manage_session',hod_views.manage_session,name="manage_session"),
    path('add_session_save',hod_views.add_session_save,name="add_session_save"),
    path('check_user_email',hod_views.check_user_email,name="check_user_email"),
    path('check_username',hod_views.check_username,name="check_username"),
    path('student_feedback_msg',hod_views.student_feedback_msg,name="student_feedback_msg"),
    path('staff_feedback_msg',hod_views.staff_feedback_msg,name="staff_feedback_msg"),
    path('student_feedback_msg_replied',hod_views.student_feedback_msg_replied,name="student_feedback_msg_replied"),
    path('staff_feedback_msg_replied',hod_views.staff_feedback_msg_replied,name="staff_feedback_msg_replied"),
    path('student_leave_reply',hod_views.student_leave_reply,name="student_leave_reply"),
    path('student_approved_leave/<str:leave_id>',hod_views.student_approved_leave,name="student_approved_leave"),
    path('student_disapproved_leave/<str:leave_id>',hod_views.student_disapproved_leave,name="student_disapproved_leave"),
    path('staff_leave_reply',hod_views.staff_leave_reply,name="staff_leave_reply"),
    path('staff_approved_leave/<str:leave_id>',hod_views.staff_approved_leave,name="staff_approved_leave"),
    path('staff_disapproved_leave/<str:leave_id>',hod_views.staff_disapproved_leave,name="staff_disapproved_leave"),
    path('admin_view_attendance',hod_views.admin_view_attendance,name="admin_view_attendance"),
    path('admin_get_attendance_date',hod_views.admin_get_attendance_date,name="admin_get_attendance_date"),
    path('admin_get_attendance_student',hod_views.admin_get_attendance_student,name="admin_get_attendance_student"),
    path('admin_profile',hod_views.admin_profile,name="admin_profile"),
    path('admin_profile_save',hod_views.admin_profile_save,name="admin_profile_save"),
    path('admin_send_notification_student',hod_views.admin_send_notification_student,name="admin_send_notification_student"),
    path('admin_send_notification_staff',hod_views.admin_send_notification_staff,name="admin_send_notification_staff"),
    path('send_student_notification',hod_views.send_student_notification,name="send_student_notification"),
    path('send_staff_notification',hod_views.send_staff_notification,name="send_staff_notification"),
    # path('datatable',hod_views.datatable,name='datatable'),

    # staff url
    path('staff_home', staffviews.staff_home, name="staff_home"),
    path('staff_take_attendance', staffviews.staff_take_attendance, name="staff_take_attendance"),
    path('staff_update_attendance', staffviews.staff_update_attendance, name="staff_update_attendance"),
    path('get_students', staffviews.get_students, name="get_students"),
    path('save_attendance_data', staffviews.save_attendance_data, name="save_attendance_data"),
    path('get_attendance_date', staffviews.get_attendance_date, name="get_attendance_date"),
    path('get_attendance_student', staffviews.get_attendance_student, name="get_attendance_student"),
    path('save_updateattendance_student', staffviews.save_updateattendance_student, name="save_updateattendance_student"),
    path('staff_apply_leave', staffviews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', staffviews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback', staffviews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save', staffviews.staff_feedback_save, name="staff_feedback_save"),
    path('staff_profile',staffviews.staff_profile,name="staff_profile"),
    path('staff_profile_save',staffviews.staff_profile_save,name="staff_profile_save"),
    path('staff_fcmtoken_save',staffviews.staff_fcmtoken_save,name="staff_fcmtoken_save"),
    path('staff_all_notification',staffviews.staff_all_notification,name="staff_all_notification"),
    path('staff_add_result',staffviews.staff_add_result,name="staff_add_result"),
    path('result_save',staffviews.result_save,name="result_save"),
    path('edit_student_result',EditResultViewClass.as_view(),name="edit_student_result"),
    path('fetch_student_result',staffviews.fetch_student_result,name="fetch_student_result"),
    # path('start_live_classroom',staffviews.start_live_classroom, name="start_live_classroom"),
    # path('start_live_classroom_process',staffviews.start_live_classroom_process, name="start_live_classroom_process"),

    # student url
    path('student_home', student_views.student_home, name="student_home"),
    path('student_view_attendance', student_views.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_save', student_views.student_view_attendance_save, name="student_view_attendance_save"),
    path('student_apply_leave', student_views.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save', student_views.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback', student_views.student_feedback, name="student_feedback"),
    path('student_feedback_save', student_views.student_feedback_save, name="student_feedback_save"),
    path('student_profile',student_views.student_profile,name="student_profile"),
    path('student_profile_save',student_views.student_profile_save,name="student_profile_save"),
    path('student_fcmtoken_save',student_views.student_fcmtoken_save,name="student_fcmtoken_save"),
    path('firebase-messaging-sw.js',student_views.showFirebaseJS,name="showFirebase_JS"),
    path('student_all_notification',student_views.student_all_notification,name="student_all_notification"),
    path('student_view_result',student_views.student_view_result,name="student_view_result"),
    path('unit_registration',student_views.unit_registration,name="unit_registration"),
    # path('join_class_room/<int:subject_id>/<int:session_year_id>',student_views.join_class_room,name="join_class_room"),
    # path('node_modules/canvas-designer/widget.html',staffviews.returnHtmlWidget,name="returnHtmlWidget"),


    # admin
    path('home',admin_views.home,name="home"),
    path('add_hod',admin_views.add_hod,name="add_hod"),
    path('add_hod_save',admin_views.add_hod_save,name="add_hod_save"),
    path('manage_hod',admin_views.manage_hod,name="manage_hod"),
    path('delete_hod/<int:id>',admin_views.delete_hod,name="delete_hod"),
    path('delete_staff/<int:id>',admin_views.delete_staff,name="delete_staff"),
    path('delete_student/<int:id>',admin_views.delete_student,name="delete_student"),
    path('Staff',admin_views.Staff,name="Staff"),
    path('Student',admin_views.Student,name="Student"),

    ]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

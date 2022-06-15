import django_filters
from django_filters import CharFilter
from django import forms
# from django.utils.translation import ugettext as_
from django.forms.utils import flatatt
from .models import courses, subject, students, hod, staff, feedbackstudent, feedbackstaff, notificationstaff


class StudentFilter(django_filters.FilterSet):
    admin__username=django_filters.CharFilter(field_name='admin__username',lookup_expr='icontains',widget=forms.TextInput(attrs={"class":"form-control border-0", "type":"search", "placeholder":"Search", "aria-label":"Search"}))
    class Meta:
        model = students
        fields = ['admin__username']

class CourseFilter(django_filters.FilterSet):
    course_name=django_filters.CharFilter(field_name='course_name',lookup_expr='icontains',widget=forms.TextInput(attrs={"class":"form-control border-0", "type":"search", "placeholder":"Search", "aria-label":"Search"}))
    class Meta:
        model = courses
        fields = ['course_name']

class SubjectFilter(django_filters.FilterSet):
    code=django_filters.CharFilter(field_name='code',lookup_expr='icontains',widget=forms.TextInput(attrs={"class":"form-control border-0", "type":"search", "placeholder":"Search", "aria-label":"Search"}))
    class Meta:
        model = subject
        fields = [
            'code'
        ]

class HodFilter(django_filters.FilterSet):
    admin__username = django_filters.CharFilter(field_name='admin__username', lookup_expr='icontains',widget=forms.TextInput(attrs={"class":"form-control border-0", "type":"search", "placeholder":"Search", "aria-label":"Search"}))
    class Meta:
        model = hod
        fields = ['admin__username']

class StaffFilter(django_filters.FilterSet):
    admin__username = django_filters.CharFilter(field_name='admin__username', lookup_expr='icontains',widget=forms.TextInput(attrs={"class":"form-control border-0", "type":"search", "placeholder":"Search", "aria-label":"Search"}))
    class Meta:
        model = staff
        fields = ['admin__username']


class StudentFeedbackFilter(django_filters.FilterSet):
    student_id__admin__username = django_filters.CharFilter(field_name='student_id__admin__username', lookup_expr='icontains',widget=forms.TextInput(attrs={"class":"form-control border-0", "type":"search", "placeholder":"Search", "aria-label":"Search"}))
    class Meta:
        model = feedbackstudent
        fields = ['student_id__admin__username']

class StaffFeedbackFilter(django_filters.FilterSet):
    staff_id__admin__username = django_filters.CharFilter(field_name='staff_id__admin__username', lookup_expr='icontains',widget=forms.TextInput(attrs={"class":"form-control border-0", "type":"search", "placeholder":"Search", "aria-label":"Search"}))
    class Meta:
        model = feedbackstaff
        fields = ['staff_id__admin__username']

class StaffNotificationFilter(django_filters.FilterSet):
    staff_id__admin__username = django_filters.CharFilter(field_name='staff_id__admin__username', lookup_expr='icontains',widget=forms.TextInput(attrs={"class":"form-control border-0", "type":"search", "placeholder":"Search", "aria-label":"Search"}))
    class Meta:
        model = notificationstaff
        fields = ['staff_id__admin__username']

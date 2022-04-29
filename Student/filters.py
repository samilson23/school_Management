import django_filters

from .models import CustomUser, courses, subject


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = "__all__"

class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = courses
        fields = "__all__"

class SubjectFilter(django_filters.FilterSet):
    class Meta:
        model = subject
        fields = ['subject_name','stage']
from django.urls import path
from .student_views import pdf_render_view, Result_List_View

app_name = 'Student'

urlpatterns = [
    # path('',Result_List_View,name='result-view'),
    path('',pdf_render_view,name='result-pdf-view'),
]
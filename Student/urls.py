from django.urls import path
from .student_views import student_render_pdf_view,student_view_result

app_name='Student'

urlpatterns = [
    # path('pdf2/',CustomerListView,name="exam_list_view"),
    path('pdf2/pdf/<id>',student_render_pdf_view,name="exam_card_view"),
    path('',student_view_result,name="transcript_view"),
]
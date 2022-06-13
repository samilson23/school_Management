from django.urls import path
from .student_views import CustomerListView,student_render_pdf_view,student_render_result_view,ResultListView

app_name='Student'

urlpatterns = [
    path('',CustomerListView,name="exam_list_view"),
    path('pdf/<id>',student_render_pdf_view,name="exam_card_view"),
    path('transcript/',ResultListView,name="transcript_view"),
    path('transcript/transc/<id>/<semester_id>',student_render_result_view,name="transcript_view"),
]
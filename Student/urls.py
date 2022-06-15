from django.urls import path
from .student_views import CustomerListView,student_render_pdf_view,student_render_result_view,ResultListView

app_name='Student'

urlpatterns = [
    path('pdf2/',CustomerListView,name="exam_list_view"),
    path('pdf2/pdf/<id>',student_render_pdf_view,name="exam_card_view"),
    path('transcript/',ResultListView,name="transcript_view"),
    path('transcript/result/<id>/<stage_id>',student_render_result_view,name="Trans"),
]
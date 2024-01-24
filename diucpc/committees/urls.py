from django.urls import path

from . import views

app_name = "committees"
urlpatterns = [
    path("student/", views.StudentCommitteListAPIView.as_view(), name="student_list"),
    path("teacher/", views.TeacherCommitteListAPIView.as_view(), name="teacher_list"),
]

from django.urls import path
from django.contrib import admin
from student_api import views


urlpatterns = [
    path('timetables/', views.get_timetable),
    path('subjects/', views.get_subject_list),
    path('attendances/subject/<int:pk>/', views.subject_wise_attendance),
]
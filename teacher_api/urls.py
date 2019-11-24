from django.urls import path
from django.contrib import admin
from teacher_api import views


urlpatterns = [
    path('verify_token/', views.verify_token),
    path('main_sections/', views.main_section_list),
    path('sections/<int:main_section_pk>/', views.section_list),
    path('frontend/', views.login_page, name="login"),
    path('frontend/teacher_list/', views.teacher_list, name="teachers-list"),
]
"""BasDB_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from users import views as user_views
from attendance import views as attendance_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('departments/', user_views.DepartmentListCreateView.as_view(), name="department-list-create"),
    path('departments/<int:pk>/', user_views.DepartmentDetailDeleteUpdateView.as_view(), name="department-detail"),

    path('main_sections/', user_views.MainSectionListCreateView.as_view(), name="main-section-list-create"),
    path('main_sections/<int:pk>/', user_views.MainSectionDetailView.as_view(), name="main-section-detail"),

    path('sections/', user_views.SectionListCreateView.as_view(), name="section-list-create"),
    path('sections/<int:pk>/', user_views.SectionDetailView.as_view(), name="section-detail"),

    path('students/', user_views.student_list_create_view, name="student-list-create"),
    path('students/<int:pk>/', user_views.StudentDetailView.as_view(), name="student-detail"),

    path('teachers/', user_views.teacher_list_create_view, name="teacher-list-create"),
    path('teachers/<int:pk>/', user_views.TeacherDetailView.as_view(), name="teacher-detail"),

    path('subjects/', attendance_views.subject_list_create_view, name="subject-list-create"),
    path('subjects/<int:pk>/', attendance_views.SubjectDetailDeleteUpdateView.as_view(), name="subject-detail"),

    path('timetable_periods/', attendance_views.TimetablePeriodListCreateView.as_view(),
         name="timetable_period-list-create"),
    path('timetable_periods/<int:pk>/', attendance_views.TimetablePeriodDetailDeleteUpdateView.as_view(),
         name="timetable_period-detail"),


]

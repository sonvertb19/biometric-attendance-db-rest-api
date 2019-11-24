from users import serializers
from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import ValidationError
from attendance.models import Subject
from users.models import Student, User, Department, Teacher, Section, MainSection


# class UserRoleSpecificPermission(permissions.BasePermission):
#     """
#         Admin: All create, list, retrieve, delete, update all objects.
#         Students: Should be allowed to view their *userDetails*, *subjects*, *timetable*, *attendances*
#         Teachers: Should be allowed to view their *userDetails*, *TimetablePeriods* they teach
#                     and the *corresponding attendances*.
#     """
#     ADMIN = 0
#     STUDENT = 1
#     TEACHER = 2
#
#     def has_permission(self, request, view):
#         # Check if the user is admin or student or teacher.
#         if request.user.is_staff:
#             user_type = self.ADMIN
#             return True
#         elif Student.objects.filter(user=request.user).count() == 1:
#             user_type = self.STUDENT
#
#         elif Teacher.objects.filter(user=request.user).count() == 1:
#             user_type = self.TEACHER
#
#         ToBeCompleted


class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = serializers.DepartmentSerializer


class DepartmentDetailDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = serializers.DepartmentSerializer


class MainSectionListCreateView(generics.ListCreateAPIView):
    queryset = MainSection.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        # print(self.request.method)
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.MainSectionReadSerializer
        else:
            return serializers.MainSectionWriteSerializer


class MainSectionDetailView(generics.RetrieveAPIView):
    queryset = MainSection.objects.all()
    permissions = [IsAdminUser]
    serializer_class = serializers.MainSectionReadSerializer


class SectionListCreateView(generics.ListCreateAPIView):
    queryset = Section.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = serializers.SectionSerializer


class SectionDetailView(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    permissions = [IsAdminUser]
    serializer_class = serializers.SectionSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def student_list_create_view(request):
    if request.method == "GET":
        if('section' in request.query_params):
            section_id = request.query_params['section']
            print(section_id)
            students = [student for student in Student.objects.filter(section=section_id)]
        else:
            students = [student for student in Student.objects.all()]

        s = serializers.StudentReadSerializer(students, many=True)
        # print(s.is_valid())
        # print(s.data)

        return Response(s.data)
    elif request.method == "POST":
        data = request.data
        s = serializers.StudentSerializer(data=data)
        if s.is_valid():
            student = s.save()

            # vd = s.validated_data
            # u = User.objects.get(username=vd['user']['username'])
            # s = Student.objects.get(user=u)
            # s = serializers.StudentReadSerializer(s)
            # return Response(s.data, status=200)

            d = s.data
            # print(d)
            user = d.get('user')
            section = Section.objects.get(name=d['section'])
            subjects = Subject.objects.filter(section=section)
            for subject in subjects:
                print(subject)
                student.subjects.add(subject)
            print(section)
            user.pop('password')
            user.pop('groups')

            d.pop('subjects')

            return Response(d, status=201)
        else:
            return Response(s.errors, status=400)


class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = serializers.StudentReadSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def teacher_list_create_view(request):
    if request.method == "GET":
        teachers = [teacher for teacher in Teacher.objects.all()]

        s = serializers.TeacherReadSerializer(teachers, many=True)
        # print(s.is_valid())
        # print(s.data)

        return Response(s.data)
    elif request.method == "POST":
        data = request.data
        s = serializers.TeacherSerializer(data=data)
        if s.is_valid():
            s.save()
            d = s.data
            vd = s.validated_data
            # print(d)
            user = d.get('user')
            user.pop('password')
            user.pop('groups')
            # print(vd)

            return Response(d, status=201)
        else:
            print(s.errors)
            return Response(s.errors, status=400)


class TeacherDetailView(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = serializers.TeacherReadSerializer
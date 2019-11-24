from users.models import Student, Section
from attendance import serializers
from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from attendance.models import Subject, TimetablePeriod, Attendance


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def subject_list_create_view(request):
    if request.method == "GET":
        subjects = [s for s in Subject.objects.all()]

        serialized_subjects = serializers.SubjectSerializer(subjects, many=True)

        return Response(serialized_subjects.data)
    elif request.method == "POST":
        """
        1. Create a subject object.
        2. Find all students who belongs to the same section to whom the subject is taught to.
        3. Add the subject to Student.subjects m2m field.
        """

        data = request.data
        s = serializers.SubjectSerializer(data=data)
        # subject.is_valid()

        # print("errors:")
        # print(subject.errors)
        # print("errors:")

        if s.is_valid():
            # print(subject.validated_data['section'].id)
            subject = s.save()

            # find students.
            section_id = s.validated_data['section'].id
            # print(section_id)
            section = Section.objects.get(id=section_id)
            student_list = Student.objects.filter(section=section)
            # print(student_list)
            for student in student_list:
                # print("adding subject:" + str(subject) + "to student: " + str(student))
                student.subjects.add(subject)
            return Response(s.data, status=201)
        else:
            print(s.errors)
            return Response(s.errors, status=400)


class SubjectDetailDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = serializers.SubjectSerializer


class TimetablePeriodListCreateView(generics.ListCreateAPIView):
    queryset = TimetablePeriod.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = serializers.TimetablePeriodSerializer


class TimetablePeriodDetailDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimetablePeriod.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = serializers.TimetablePeriodSerializer

class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = serializers.AttendanceSerializer


class AttendanceDetailDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = serializers.AttendanceSerializer
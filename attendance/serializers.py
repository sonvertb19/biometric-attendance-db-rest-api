from rest_framework import serializers
from attendance.models import Subject, TimetablePeriod
from users.serializers import SectionSerializer, TeacherSerializer, StudentReadSerializer
from attendance.models import Attendance
from users.models import Section, Teacher

from datetime import datetime as dt

class SubjectSerializer(serializers.ModelSerializer):
    section = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="name",
        queryset=Section.objects.all()
    )

    class Meta:
        model = Subject
        fields = '__all__'

class SubjectSerializerId(serializers.ModelSerializer):
    section = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="id",
    )

    class Meta:
        model = Subject
        fields = '__all__'

class SectionSerializerForStudentAPI(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class TimetablePeriodSerializer(serializers.ModelSerializer):
    # subject = serializers.SlugRelatedField(
    #     many=False,
    #     read_only=False,
    #     slug_field="title",
    #     queryset=Subject.objects.all()
    # )
    class Meta:
        model = TimetablePeriod
        # fields = '__all__'
        exclude = ['section']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['subject'] = SubjectSerializerId(instance.subject).data
        response['teacher'] = TeacherSerializer(instance.teacher).data['user']['first_name']
        # print(instance.section)
        response['section'] = SectionSerializer(instance.section).data['name']
        return response

class TimetablePeriodSerializerForStudentAPI(serializers.ModelSerializer):
    class Meta:
        model = TimetablePeriod
        # fields = '__all__'
        exclude = ['section', 'id', 'teacher']

    def to_representation(self, instance):
        day_int_to_str = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }
        response = super().to_representation(instance)
        response['subject'] = SubjectSerializerId(instance.subject).data['title']
        response['day'] = day_int_to_str[int(instance.day)]
        # response['teacher'] = TeacherSerializer(instance.teacher).data['user']['first_name']
        # print(instance.section)
        return response

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)

        # create a field called value_str
        value_str = ""
        if int(instance.value) == 1:
            value_str = "Present"
        elif int(instance.value) == 0:
            value_str = "Absent"

        student_object = StudentReadSerializer(instance.student).data
        custom_student_object = {
            "id": student_object["id"],
            "username": student_object["user"]["username"],
            "first_name": student_object["user"]["first_name"],
            "last_name": student_object["user"]["last_name"]
            }

        timetable_period_object = TimetablePeriodSerializer(instance.timetable_period).data
        custom_timetable_period_object = {
            "id": timetable_period_object["id"],
            "subject": timetable_period_object["subject"]["title"],
            "section": timetable_period_object["section"],
            }

        response['student'] = custom_student_object
        response['timetable_period'] = custom_timetable_period_object
        response['value_str'] = value_str
        return response

class AttendanceSerializerForStudentAPI(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        exclude = ['value', 'timetable_period', 'student']

    def to_representation(self, instance):
        response = super().to_representation(instance)

        # create a field called value_str
        value_str = ""
        if int(instance.value) == 1:
            value_str = "Present"
        elif int(instance.value) == 0:
            value_str = "Absent"

        response['value_str'] = value_str
        
        # create a field called time
        timetable_period_object = TimetablePeriodSerializer(instance.timetable_period).data
        time = timetable_period_object['time']
        response['time'] = time



        # create a field called day
        day = instance.date.weekday()
        day_int_to_str = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }
        response['day'] = day_int_to_str[day]
        
        return response
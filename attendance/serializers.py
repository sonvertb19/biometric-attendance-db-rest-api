from rest_framework import serializers
from attendance.models import Subject, TimetablePeriod
from users.serializers import SectionSerializer, TeacherSerializer
from users.models import Section, Teacher


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


class TimetablePeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetablePeriod
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['subject'] = SubjectSerializer(instance.subject).data
        response['teacher'] = TeacherSerializer(instance.teacher).data['user']['first_name']
        return response

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

class SubjectSerializerId(serializers.ModelSerializer):
    section = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="id",
    )

    class Meta:
        model = Subject
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

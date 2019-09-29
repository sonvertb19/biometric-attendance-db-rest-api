from users.models import Student, User, Department, Teacher, Section, MainSection
from rest_framework import serializers
# from attendance import serializers as attendance_serializers
from attendance.models import Subject


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class MainSectionWriteSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=Department.objects.all()
    )

    class Meta:
        model = MainSection
        fields = '__all__'


class MainSectionReadSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="name",
        queryset=Department.objects.all()
    )

    class Meta:
        model = MainSection
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    main_section = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="name",
        queryset=MainSection.objects.all()
    )

    class Meta:
        model = Section
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'groups', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).count():
            raise serializers.ValidationError("Email Already Registered")
        return value

    def create(self, validated_data):
        # print("creating user")
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    section = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="name",
        queryset=Section.objects.all()
    )

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        u = UserSerializer(data=user)
        u.is_valid()
        u.save()
        student = Student.objects.create(user=User.objects.get(id=u.data['id']), **validated_data)
        return student


class StudentReadSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    user = UserReadSerializer()
    subjects = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="title"
    )

    class Meta:
        model = Student
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        u = UserSerializer(data=user)
        u.is_valid()
        u.save()

        teacher = Teacher.objects.create(user=User.objects.get(id=u.data['id']))

        return teacher


class TeacherReadSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'

from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)


class MainSection(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class Section(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    main_section = models.ForeignKey(MainSection, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} of {1}".format(self.name, self.main_section.name)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, unique=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('attendance.Subject', null=True)

    def __str__(self):
        return "{0}:{1}".format(self.user.username, self.user.get_full_name())


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, unique=True)

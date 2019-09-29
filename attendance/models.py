from django.db import models


class Subject(models.Model):
    title = models.CharField(max_length=100, null=False)
    section = models.ForeignKey('users.Section', on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together = ['section', 'title']


class TimetablePeriod(models.Model):
    DAY_CHOICES = [
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday')
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    day = models.CharField(max_length=1, choices=DAY_CHOICES, null=False)
    time = models.TimeField(null=False)

    class Meta:
        unique_together = ['day', 'time']


# class Attendance(models.Model):
#     VALUE_CHOICES = [
#         (0, 'Not Marked'),
#         (1, 'Present'),
#         (2, 'Absent'),
#         (3, 'Cancelled')
#     ]
#     timetable_period = models.ForeignKey(TimetablePeriod, on_delete=models.CASCADE)
#     value = models.CharField(max_length=1, choices=VALUE_CHOICES, null=False)
#     student = models.ForeignKey('users.Student', on_delete=models.CASCADE)

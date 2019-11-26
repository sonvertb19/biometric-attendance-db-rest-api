from django.db import models


class Subject(models.Model):
    title = models.CharField(max_length=100, null=False)
    section = models.ForeignKey('users.Section', on_delete=models.CASCADE, null=False)

    class Meta:
        # unique_together = ['title']
        unique_together = ['section', 'title']


class TimetablePeriod(models.Model):
    DAY_CHOICES = [
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday')
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    day = models.CharField(max_length=1, choices=DAY_CHOICES, null=False)
    time = models.TimeField(null=False)
    section = models.ForeignKey('users.Section', on_delete=models.CASCADE, null=False)


    def save(self, *args, **kwargs):
        # A seperate section field is required but
        # can not rely on frontend developer to provide
        # same section in the seperate section field as well as the subject field
        self.section = self.subject.section
        super().save(*args, **kwargs)

    class Meta:
        # unique_together = ['day', 'time']
        unique_together = ['day', 'time', 'section']

class Attendance(models.Model):
    VALUE_CHOICES = [
        (-1, 'Not Marked'),
        (1, 'Present'),
        (0, 'Absent'),
        (2, 'Cancelled')
    ]
    timetable_period = models.ForeignKey(TimetablePeriod, on_delete=models.CASCADE)
    value = models.CharField(max_length=1, choices=VALUE_CHOICES, null=False)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    date = models.DateField(null=False)
from attendance.models import TimetablePeriod as t

for x in t.objects.all():
	x.delete()

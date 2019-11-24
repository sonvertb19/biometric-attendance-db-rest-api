from rest_framework.decorators import api_view
from rest_framework import response
import requests as rq

from oauth2_provider.models import AccessToken
from users.models import Teacher, Section, Student
from attendance.models import TimetablePeriod, Subject, Attendance
from attendance.serializers import (TimetablePeriodSerializerForStudentAPI, 
									SectionSerializerForStudentAPI,
									AttendanceSerializerForStudentAPI)

def get_student(token):

	# token contains: Bearer XXXXXXXXX
	token = token.split()
	token = token[1]

	# print(token)
	token = str(token)
	token_list = AccessToken.objects.filter(token=token)

	student = None

	if len(token_list) > 0:
		# Check if the user is teacher or not
		user = token_list[0].user
		if len(Student.objects.filter(user=user)) > 0:
			return Student.objects.filter(user=user)[0]
		else:
			print("user is not a student user")
			return -1

	return student

@api_view(["GET"])
def get_timetable(request):

	if 'Authorization' in request.headers:
		student = get_student(request.headers['Authorization'])

		if student == None:
			return response.Response(status=401)
		elif student == -1:
			return response.Response({"Forbidden":"Not a student"}, status=403)
		else:
			subjects = [ subject for subject in student.subjects.all() ]
			timetable_list = []
			for subject in subjects:
				for timetable in TimetablePeriod.objects.filter(subject=subject):
					timetable_list.append(timetable)

			serialized_timetable_list = []
			for timetable in timetable_list:
				serialized_timetable_list.append(TimetablePeriodSerializerForStudentAPI(timetable).data)


			# timetables = [ timetable for timetable in ]
			return response.Response(serialized_timetable_list, status=200)

	else:
		return response.Response({"headers": "No Authorization Header"}, status=400)


@api_view(["GET"])
def get_subject_list(request):
	if 'Authorization' in request.headers:
		student = get_student(request.headers['Authorization'])

		if student == None:
			return response.Response(status=401)
		elif student == -1:
			return response.Response({"Forbidden":"Not a student"}, status=403)
		else:
			serialized_subject_list = []
			for subject in student.subjects.all():
				serialized_subject_list.append(SectionSerializerForStudentAPI(subject).data)
			return response.Response(serialized_subject_list, status=200)

	else:
		return response.Response({"headers": "No Authorization Header"}, status=400)


@api_view(["GET"])
def subject_wise_attendance(request, **kwargs):
	subject_pk = kwargs['pk']

	if 'Authorization' in request.headers:
		student = get_student(request.headers['Authorization'])

		if student == None:
			return response.Response(status=401)
		elif student == -1:
			return response.Response({"Forbidden":"Not a student"}, status=403)
		else:
			attendance_list = []
			serialized_attendance_list = []
			# Check if subject with id = subject_pk exists.
			subject_list = Subject.objects.filter(id=subject_pk)
			if len(subject_list) > 0:
				# subject exists
				subject = subject_list[0]
				for timetable in TimetablePeriod.objects.filter(subject=subject):
					for attendance in Attendance.objects.filter(student=student, timetable_period=timetable):
						attendance_list.append(attendance)

				for attendance in attendance_list:
					serialized_attendance = AttendanceSerializerForStudentAPI(attendance)
					serialized_attendance_list.append(serialized_attendance.data)
				return response.Response(serialized_attendance_list, status=200)
			else:
				not_found_error = "Subject with pk = {0} does not exist".format(subject_pk)
				return response.Response({"not_found":not_found_error}, status=404)

	else:
		return response.Response({"headers": "No Authorization Header"}, status=400)

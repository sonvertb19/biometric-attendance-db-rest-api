from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import response
import requests as rq
from oauth2_provider.models import AccessToken
from users.models import Teacher

from users.models import MainSection, Section
from users.serializers import MainSectionReadSerializer

from attendance.models import TimetablePeriod
from attendance.serializers import SectionSerializerForStudentAPI

import json
from datetime import datetime as dt
# Create your views here.
@api_view(["GET"])
def verify_token(request):
	# check if token exists.
	# id not: reply with 400.
	if 'token' in request.data:
		token = request.data["token"]
		token_list = AccessToken.objects.filter(token=token)
		if len(token_list) > 0:
			return response.Response(data={"active":True}, status=200)
		else:
			return response.Response(data={"active":False}, status=401)

	else:
		return response.Response(data={"token": "This field is required"}, status=400)

def get_teacher_user(token):
	# token contains: Bearer XXXXXXXXX
	token = token.split()
	token = token[1]

	token = str(token)
	token_list = AccessToken.objects.filter(token=token)

	teacher_user = None

	if len(token_list) > 0:
		# Check if the user is teacher or not
		user = token_list[0].user
		if len(Teacher.objects.filter(user=user)) > 0:
			return user
		else:
			print("user is not a teacher user")
			return -1

	return teacher_user

@api_view(['GET'])
def main_section_list(request):
	if 'Authorization' in request.headers:
		teacher_user = get_teacher_user(request.headers['Authorization'])

		if teacher_user == None:
			return response.Response(status=401)
		elif teacher_user == -1:
			return response.Response({"Forbidden":"Not a teacher"},status=403)
		else:
			
			main_sections = [ main_section for main_section in MainSection.objects.all()]

			main_sections = MainSectionReadSerializer(MainSection.objects.all(), many=True)
			main_sections = main_sections.data

			main_sections_list = []

			for main_section in main_sections:
				main_section = dict(main_section)
				main_sections_list.append(main_section)

			return response.Response(main_sections_list, status=200)

	else:
		return response.Response({"headers": "No Authorization Header"}, status=400)


@api_view(['POST'])
def timetable_list(request):

	if 'Authorization' in request.headers:
		teacher_user = get_teacher_user(request.headers['Authorization'])

		if teacher_user == None:
			return response.Response(status=401)
		elif teacher_user == -1:
			return response.Response({"Forbidden":"Not a teacher"},status=403)
		else:
			# Find the teacher object from teacher_user
			teacher = Teacher.objects.get(user=teacher_user)
			print(request.data)
			if 'section_list' in request.data:
				section_list = request.data['section_list']
				print(section_list)

				# Find all timetable_periods with the section, teacher, day.
				day = dt.now().date().weekday()
				day_int_to_str={
				    0: "Monday",
				    1: "Tuesday",
				    2: "Wednesday",
				    3: "Thursday",
				    4: "Friday",
				    5: "Saturday",
				    6: "Sunday",
				}
				print(day_int_to_str[day])

				array_section_id_timetable_object_list = []
				for section_id in section_list:
					timetable_list = TimetablePeriod.objects.filter(section=section_id, teacher=teacher, day=day)
					# print(timetable_list)

					# Arrays of timetable_periods in array
					section_id_timetable_object_list = {
						int(section_id): []
					}
					for timetable in timetable_list:
						timetable_id = timetable.id
						subject_title = timetable.subject.title
						time = timetable.time
						section = timetable.section.name

						timetable_object = {
							"id": int(timetable_id),
							"title": subject_title,
							"time": str(time),
							"section": section
						}
						section_id_timetable_object_list[section_id].append(timetable_object)


					# section_id_timetable_object_list is: 
					"""
						{
							section_id: [
								{id:"", time:"", subject:""},
								{id:"", time:"", subject:""}
							]
						}
					"""
					# print(section_id_timetable_object_list)
					array_section_id_timetable_object_list.append(section_id_timetable_object_list)


				print(json.dumps(array_section_id_timetable_object_list, indent=4))

				return response.Response(array_section_id_timetable_object_list, status=200)
			return response.Response(status=400)

	else:
		return response.Response({"headers": "No Authorization Header"}, status=400)


@api_view(['GET'])
def section_list(request, **kwargs):
	main_section_pk = kwargs['main_section_pk']

	if 'Authorization' in request.headers:
		teacher_user = get_teacher_user(request.headers['Authorization'])

		if teacher_user == None:
			return response.Response(status=401)
		elif teacher_user == -1:
			return response.Response({"Forbidden":"Not a teacher"},status=403)
		else:
			sections = [ section for section in Section.objects.filter(main_section=main_section_pk)]

			section_list = []

			for section in sections:
				section = SectionSerializerForStudentAPI(section).data
				section_list.append(section)

			return response.Response(section_list, status=200)

	else:
		return response.Response({"headers": "No Authorization Header"}, status=400)


def login_page(request):
	return render(request, "teacher_api/login_page.html")

def teacher_list(request):
	return render(request, "teacher_api/teachers.html")

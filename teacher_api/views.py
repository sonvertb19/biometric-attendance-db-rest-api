from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import response
import requests as rq
from oauth2_provider.models import AccessToken
from users.models import Teacher

from users.models import MainSection, Section
from users.serializers import MainSectionReadSerializer

from attendance.serializers import SectionSerializerForStudentAPI

import json

# Create your views here.
@api_view(["GET"])
def verify_token(request):
	# check if token exists.
	# id not: reply with 400.
	if 'token' in request.data:
		token = request.data["token"]
		token_list = AccessToken.objects.filter(token=token)
		if len(token_list) > 0:
			print(token_list[0].user)
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
		print("User is ", end="")
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
			print(teacher_user)
			
			main_sections = [ main_section for main_section in MainSection.objects.all()]

			main_sections = MainSectionReadSerializer(MainSection.objects.all(), many=True)
			main_sections = main_sections.data

			main_sections_list = []

			for main_section in main_sections:
				# print(main_section)
				main_section = dict(main_section)
				main_sections_list.append(main_section)

			return response.Response(main_sections_list, status=200)

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
			print(teacher_user)


			
			sections = [ section for section in Section.objects.filter(main_section=main_section_pk)]

			print(sections)

			sections = SectionSerializerForStudentAPI(Section.objects.all(), many=True)

			sections = sections.data

			sections_list = []

			for section in sections:
				# print(main_section)
				section = dict(section)
				sections_list.append(section)

			return response.Response(sections_list, status=200)

	else:
		return response.Response({"headers": "No Authorization Header"}, status=400)

	

def login_page(request):
	return render(request, "teacher_api/login_page.html")

def teacher_list(request):
	return render(request, "teacher_api/teachers.html")

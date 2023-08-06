from django.shortcuts import render

from . import models      #?
from .models import User  #우리가 커스텀한 유저 모델

from django.contrib import auth
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg import openapi 
from drf_yasg.utils import swagger_auto_schema

@csrf_exempt
def deco(requset):
    return HttpResponse("success")


class LoginView(APIView): # 로그인 관련 뷰
    @swagger_auto_schema(tags=['로그인 기능'], request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'userID': openapi.Schema(type=openapi.TYPE_STRING, description='userID'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
        },
        required=['userID', 'password']
    ), responses={200: 'Success'})
    
    def post(self, request):
        userID = request.data.get("userID")
        password = request.data.get("password")
        
        user = authenticate(request, username=userID,password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"message": "로그인 성공",
                             'token':token.key,
                             'id':user.userID,
                             '회원종류':user.user_type,
                             '이름':user.user_name,
                             '전화번호':user.user_phonenum,
                             '주소':user.user_address,
                             '성별_1남자_2여자':user.user_gender}, status=200)
            
        
        else:
            return Response({"message": "아이디 또는 비밀번호가 틀렸습니다."}, status=400)
        
        
        
class SignupView(APIView):
    @swagger_auto_schema(tags=['회원가입기능'], request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'userID': openapi.Schema(type=openapi.TYPE_STRING, description='userID'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            'user_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_type'),
            'user_name': openapi.Schema(type=openapi.TYPE_STRING, description='user_name'),
            'user_phonenum': openapi.Schema(type=openapi.TYPE_STRING, description='user_phonenum'),
            'user_address': openapi.Schema(type=openapi.TYPE_STRING, description='user_address'),
            'user_gender': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_gender'),
            
        },
        required=['userID', 'password', 'user_type', 'user_name', 'user_phonenum', 'user_address', 'user_gender']
    ), responses={200: 'Success'})

    def post(self, request):
        user = User.objects.create_user(
            userID = request.data.get("userID"),
            password = request.data.get("password"),
            user_type = request.data.get("user_type"),
            user_name = request.data.get("user_name"),
            user_phonenum = request.data.get("user_phonenum"),
            user_address = request.data.get("user_address"),
            user_gender = request.data.get("user_gender"),
        
            # userID=userID,
            # password=password,
            # user_type=user_type,
            # user_name=user_name,
            # user_phonenum=user_phonenum,
            # user_adress=user_adress,
            # user_gender=user_gender,
        )
        
        if user:
            return Response({"message": "회원가입 완료"},status=201)
        else:
            return Response({"message": "회원가입 실패"},status=400)
    


class LogoutView(APIView):
    def get(self, request):
        if request.user is not None: 
            auth.logout(request)
            return Response({"message": "로그아웃 성공"},status=200)
        else:
            return Response({"message": "로그아웃 실패"},status=403)
        
        
        
        
class MyInfo(APIView):
    @swagger_auto_schema(tags=['로그인 상태에서 내 정보 보기'])

    def get(self, request):
        user = request.user

        if user is not None:
            # return Response({"message": user.id})
            return Response({"message": user.user_name})
        else:
            return Response({"message": "로그아웃 상태입니다."})
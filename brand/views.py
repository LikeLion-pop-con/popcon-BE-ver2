from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Popup,Brand

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .serializers import PopupSerializer,BrandSerializer

from drf_yasg import openapi 
from drf_yasg.utils import swagger_auto_schema

class AllPopup_listView(APIView):
    @swagger_auto_schema(tags=['모든팝업'])
    def get(self,request):
        all_popup_list=Popup.objects.all()
        popuplistSerializer=PopupSerializer(all_popup_list,many=True)
        return Response(popuplistSerializer.data,status=200)


class OpenedPopup_listView(APIView):
    @swagger_auto_schema(tags=['오픈한팝업'])
    def get(self,request):
        opened_popup_list=Popup.objects.filter(popup_state=1)
        popuplistSerializer=PopupSerializer(opened_popup_list,many=True)
        return Response(popuplistSerializer.data,status=200)


class willOpenPopup_listView(APIView):
    @swagger_auto_schema(tags=['오픈예정팝업'])
    def get(self,request):
        willopen_popup_list=Popup.objects.filter(popup_state=2)
        popuplistSerializer=PopupSerializer(willopen_popup_list,many=True)
        return Response(popuplistSerializer.data,status=200)



class SearchView(APIView):
    @swagger_auto_schema(tags=['검색하고싶은 브랜드,팝업'])
    def get(self, request, search_name):
        # 먼저 popup_name으로 검색해봅니다.
        popups = Popup.objects.filter(popup_name__icontains=search_name)
        brands = Brand.objects.filter(brand_name__icontains=search_name)
        if popups.exists() or brands.exists():
            # popup_name이 존재하는 경우, 해당 Popup을 리턴합니다.
            popup_serializer = PopupSerializer(popups, many=True)
            brand_serializer = BrandSerializer(brands, many=True)
            combined_data = {
                "brands": brand_serializer.data,
                "popups": popup_serializer.data,
            }
            return Response(combined_data, status=200)
        else:
            # Brand도 존재하지 않는 경우 에러 메시지를 리턴합니다.
            error_message = {"message": "검색 결과가 없습니다."}
            return Response(error_message, status=404)
        

class CategoryPopup_listView(APIView):
    @swagger_auto_schema(tags=['카테고리별 popup추출main뒤에 1,2,3,4 붙이셈'])
    # @swagger_auto_schema(tags=['카테고리별 popup추출'], request_body=openapi.Schema(
    #     type=openapi.TYPE_OBJECT,
    #     properties={
    #         'input': openapi.Schema(type=openapi.TYPE_INTEGER, description='input'), 
    #     },
    #     required=['input']
    # ), responses={200: 'Success'})


    def get(self,request,input):
        if input==1:
            popups=Popup.objects.filter(popup_category=5)#스토어
            popuplistSerializer=PopupSerializer(popups,many=True)
            return Response(popuplistSerializer.data,status=200)
        elif input==2:
            popups=Popup.objects.filter(popup_category=6)#갤러리
            popuplistSerializer=PopupSerializer(popups,many=True)
            return Response(popuplistSerializer.data,status=200)
        elif input==3:
            popups=Popup.objects.filter(popup_category=7)#스테이지
            popuplistSerializer=PopupSerializer(popups,many=True)
            return Response(popuplistSerializer.data,status=200)
        elif input==4:
            popups=Popup.objects.filter(popup_category=8)#클래스
            popuplistSerializer=PopupSerializer(popups,many=True)
            return Response(popuplistSerializer.data,status=200)
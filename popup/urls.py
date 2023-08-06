"""
URL configuration for popup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from user import views
from brand.views import AllPopup_listView ,willOpenPopup_listView,OpenedPopup_listView,SearchView
from brand.views import CategoryPopup_listView
from popup_place.views import PopupPlaceView


from user.views import *

#Swagger 
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.static import serve

#image
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title = "POPCON",
        default_version = "v1",
        description = "Swagger를 사용한 API 문서입니다",
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),    
    path('signup/',SignupView.as_view()),
    path('login/',LoginView.as_view()),
    path('myinfo/',MyInfo.as_view()),
    path('logout/',LogoutView.as_view()),
    

    path('popuplist/all',AllPopup_listView.as_view()),
    path('main/<int:input>',CategoryPopup_listView.as_view(),name='input'),#카테고리 리스트
    path('popuplist/opened',OpenedPopup_listView.as_view()),
    path('popuplist/willopen',willOpenPopup_listView.as_view()),
    path('search/<str:search_name>',SearchView.as_view(),name='search_name'),
    path('popupplace/<int:pkey>',PopupPlaceView.as_view(),name='pkey'),
    

    
    # Swagger url
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),#배포
    re_path(r'^image/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # image  #이게 로컬


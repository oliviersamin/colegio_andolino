"""andolina URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from v1.views import (
    ParentViewSet,
    ChildViewSet,
    TeacherViewSet,
    GroupViewSet,
    DocumentViewSet,
    UserViewSet,
)


router = routers.SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('parents', ParentViewSet, basename='parents')
router.register('children', ChildViewSet, basename='children')
router.register('teachers', TeacherViewSet, basename='teachers')
router.register('school_groups', GroupViewSet, basename='school_groups')
router.register('documents', DocumentViewSet, basename='documents')


urlpatterns = [
    path('management/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('v1.urls', namespace='v1')),

]

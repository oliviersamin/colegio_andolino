# from django.shortcuts import render
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import (
    Child,
    Parent,
    Teacher,
    Group,
    Document,
)
# from .permissions import ClientsPermissions, ContractsPermissions, EventsPermissions
from .serializers import (
    ParentSerializer,
    ParentDetailSerializer,
    ChildSerializer,
    ChildDetailSerializer,
    TeacherSerializer,
    TeacherDetailSerializer,
    GroupDetailSerializer,
    GroupSerializer,
    DocumentSerializer,
    DocumentDetailSerializer,
    UserSerializer,
    UserDetailSerializer,
)


class BlacklistRefreshView(APIView):
    """ Blacklist all the logout token"""
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Logout performed successfully")

class UserViewSet(ModelViewSet):
    """ manage all the views related to the user default Django model """
    # permission_classes = (ClientsPermissions,)
    # search_fields = ['first_name', 'last_name', 'email']
    # filter_backends = (filters.SearchFilter,)
    serializer_class = UserSerializer
    detail_serializer_class = UserDetailSerializer

    def get_queryset(self):
        return User.objects.all().order_by('id')

    # def get_serializer_class(self):
    #     if self.action not in ['list', 'delete']:
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()


class ParentViewSet(ModelViewSet):
    """ manage all the views related to the parent model """
    # permission_classes = (ClientsPermissions,)
    # search_fields = ['first_name', 'last_name', 'email']
    # filter_backends = (filters.SearchFilter,)
    serializer_class = ParentSerializer
    detail_serializer_class = ParentDetailSerializer

    def get_queryset(self):
        return Parent.objects.all().order_by('id')

    # def get_serializer_class(self):
    #     if self.action not in ['list', 'delete']:
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()


class ChildViewSet(ModelViewSet):
    """ manage all the views related to the child model """
    # permission_classes = (ClientsPermissions,)
    # search_fields = ['first_name', 'last_name', 'email']
    # filter_backends = (filters.SearchFilter,)
    serializer_class = ChildSerializer
    detail_serializer_class = ChildDetailSerializer

    def get_queryset(self):
        return Child.objects.all().order_by('id')

    # def get_serializer_class(self):
    #     if self.action not in ['list', 'delete']:
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()


class TeacherViewSet(ModelViewSet):
    """ manage all the views related to the teacher model """
    # permission_classes = (ClientsPermissions,)
    # search_fields = ['first_name', 'last_name', 'email']
    # filter_backends = (filters.SearchFilter,)
    serializer_class = TeacherSerializer
    detail_serializer_class = TeacherDetailSerializer

    def get_queryset(self):
        return Teacher.objects.all().order_by('id')

    # def get_serializer_class(self):
    #     if self.action not in ['list', 'delete']:
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()


class GroupViewSet(ModelViewSet):
    """ manage all the views related to the school_group model """
    # permission_classes = (ClientsPermissions,)
    # search_fields = ['first_name', 'last_name', 'email']
    # filter_backends = (filters.SearchFilter,)
    serializer_class = GroupSerializer
    detail_serializer_class = GroupDetailSerializer

    def get_queryset(self):
        return Group.objects.all().order_by('id')

    # def get_serializer_class(self):
    #     if self.action not in ['list', 'delete']:
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()


class DocumentViewSet(ModelViewSet):
    """ manage all the views related to the document model """
    # permission_classes = (ClientsPermissions,)
    # search_fields = ['first_name', 'last_name', 'email']
    # filter_backends = (filters.SearchFilter,)
    serializer_class = DocumentSerializer
    detail_serializer_class = DocumentDetailSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     return_serializer = self.detail_serializer_class(instance)
    #     return Response(
    #         return_serializer.data, status=status.HTTP_201_CREATED, headers=headers
    #     )

    def get_queryset(self):
        return Document.objects.all().order_by('id')

    # def get_serializer_class(self):
    #     if self.action not in ['list', 'delete']:
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()

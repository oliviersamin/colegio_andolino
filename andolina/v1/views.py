# from django.shortcuts import render
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Child, Parent
# from .permissions import ClientsPermissions, ContractsPermissions, EventsPermissions


class BlacklistRefreshView(APIView):
    """ Blacklist all the logout token"""
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Logout performed successfully")


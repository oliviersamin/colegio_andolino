from django.contrib.auth.models import User
from rest_framework import serializers
from v1.models import Group


class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

from django.contrib.auth.models import User
from rest_framework import serializers
from v1.models import Child


class ChildDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['id', 'user', 'last_name', 'first_name',  'age', 'parents', 'tutor', 'birth_date']

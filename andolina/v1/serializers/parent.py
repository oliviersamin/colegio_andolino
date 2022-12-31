from django.contrib.auth.models import User
from rest_framework import serializers
from v1.models import Parent


class ParentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'user', 'last_name', 'first_name', 'children', 'school_status']

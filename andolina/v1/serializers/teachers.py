from django.contrib.auth.models import User
from rest_framework import serializers
from v1.models import Teacher


class TeacherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'last_name', 'first_name', 'school_email']

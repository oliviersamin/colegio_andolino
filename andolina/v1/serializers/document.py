from django.contrib.auth.models import User
from rest_framework import serializers
from v1.models import Document


class DocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['title', 'type', 'created_by', 'date_created']

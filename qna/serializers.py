from rest_framework.serializers import ModelSerializer

from .models import *

from rest_framework import serializers

class DiarySerializer(ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'

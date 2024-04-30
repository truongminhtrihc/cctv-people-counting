from rest_framework import serializers
from api.models import Metadata, Camera, DailyTotal

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = '__all__'

class DailyTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTotal
        fields = '__all__'
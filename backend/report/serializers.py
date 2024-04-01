from rest_framework import serializers
from report.models import Metadata, Camera

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
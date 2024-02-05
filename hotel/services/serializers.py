from rest_framework import serializers
from .models import *

class ServiceSerializer(serializers.ModelSerializer):
    service_type_name = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = '__all__'

    def get_service_type_name(self, obj):
        return obj.service_type.name

class ServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceType
        fields = '__all__'

class ParkingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingSpace
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = '__all__'
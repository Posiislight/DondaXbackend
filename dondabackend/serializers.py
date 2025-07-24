from .models import MotorcycleOrder
from rest_framework import serializers

class MotorcycleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotorcycleOrder
        fields = '__all__'
        read_only_fields = ['id','created_at']
        
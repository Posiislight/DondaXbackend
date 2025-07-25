from .models import MotorcycleOrder,EmailList
from rest_framework import serializers

class MotorcycleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotorcycleOrder
        fields = '__all__'
        read_only_fields = ['id','created_at']
        
class EmailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailList
        fields = '__all__'
        read_only_fields = ['id','joined_at']
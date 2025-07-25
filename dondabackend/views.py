from tokenize import Octnumber
from django.shortcuts import render
from .models import MotorcycleOrder,EmailList
from .serializers import MotorcycleOrderSerializer,EmailListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import json

class BookingsView(APIView):
    def post(self, request):
        serializer = MotorcycleOrderSerializer(data=request.data)
        try:
            if serializer.is_valid():
                order = serializer.save()

                # Format additional features
                features = json.dumps(order.additional_features, indent=2) if order.additional_features else "None"

                # Construct email message
                message = f"""
New Motorcycle Order

Customer Information:
Name: {order.first_name} {order.last_name}
Email: {order.email}
Phone: {order.phone}
Address: {order.address}
City: {order.city}
Zip Code: {order.zip_code}

Order Details:
Model: {order.motorcycle_model}
Color: {order.color}
Quantity: {order.quantity}
Frequency: {order.frequency}
Additional Features: {features}

Submitted on: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}
"""

                # Send email

                try:
                    order_count = MotorcycleOrder.objects.count()
                    order_number = order_count+1
                    send_mail(
                        subject=f"Order {order_number} New Motorcycle Order Received",
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=["adelekeolamiposi@gmail.com"],  # or your admin/support email
                        fail_silently=False,
                    )
                except Exception as e:
                    
                    return Response(serializer.errors,status=401)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class EmailList(APIView):
    def post(self,request):
        serializer = EmailListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data,status=200)
        else:
            return Response(serializer.errors,status=400)
        
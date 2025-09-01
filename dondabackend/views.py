
from django.shortcuts import render
from .models import MotorcycleOrder,EmailList
from .serializers import MotorcycleOrderSerializer,EmailListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import json
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.http import JsonResponse

load_dotenv()  # if using dotenv
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")


def send_email(to_email, subject, html_content):
    message = Mail(
        from_email='enquiry@dondaxlimited.com',  # Must be verified sender
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"Email sent: {response.status_code}")
        return True
    except Exception as e:
        print(f"SendGrid error: {e}")
        return False

class BookingsView(APIView):
    def post(self, request):
        serializer = MotorcycleOrderSerializer(data=request.data)
        try:
            if serializer.is_valid():
                order = serializer.save()

                # Format additional features
                features = json.dumps(order.additional_features, indent=2) if order.additional_features else "None"



                # Send email

                try:
                    order_count = MotorcycleOrder.objects.count()
                    order_number = order_count+1
                    html_message = f"""
                        <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.5;">
                        <h2>New Motorcycle Order</h2>
                        <h3>Customer Information:</h3>
                        <p>Name: {order.first_name} {order.last_name}<br>
                        Email: {order.email}<br>
                        Phone: {order.phone}<br>
                        Address: {order.address}<br>
                        City: {order.city}<br>
                        Zip Code: {order.zip_code}</p>

                        <h3>Order Details:</h3>
                        <p>Model: {order.motorcycle_model}<br>
                        Color: {order.color}<br>
                        Quantity: {order.quantity}<br>
                        Frequency: {order.frequency}<br>
                        Additional Features: {features}</p>

                        <p>Submitted on: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                </body>
</html>
"""
                    send_email(
                        to_email='enquiry@dondaxlimited.com',
                        subject=f"Order {order_number} submitted",
                        html_content = html_message

                    )
                except Exception as e:
                    
                    return Response({'email error': str(e)},status=401)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=200)
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
        
def ping(request):
    return JsonResponse({"status":"ok"},status=200)
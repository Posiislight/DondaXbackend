from django.urls import path


from . import views

urlpatterns = [
    path('bookings/',views.BookingsView.as_view())
]
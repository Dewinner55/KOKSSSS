from django.urls import path

from . import views

urlpatterns = [
    path('bookings/', views.BookingListCreateAPIView.as_view(), name='bookings'),
    path('bookings/confirm/', views.BookingConfirmationAPIView.as_view(), name='booking_confirmation'),
    path('bookings/history/', views.UserBookingHistoryAPIView.as_view(), name='booking_history'),
]
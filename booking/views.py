from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Booking
from .serializers import BookingSerializer
from rest_framework import generics, status
from rest_framework.response import Response


class BookingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        if not booking.is_apartment_available():
            raise ValidationError("Квартира уже забронирована на выбранные даты.")
        booking.send_confirmation_email()  # Убедитесь, что вызывается этот метод

class BookingConfirmationAPIView(generics.GenericAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs):
        confirmation_code = request.data.get('confirmation_code')

        try:
            booking = self.queryset.get(user=request.user, confirmation_code=confirmation_code)
        except Booking.DoesNotExist:
            return Response({"error": "Бронирование не найдено."}, status=status.HTTP_404_NOT_FOUND)

        if booking.activate_booking(confirmation_code):
            return Response({"success": "Бронирование подтверждено."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Неправильный код подтверждения."}, status=status.HTTP_400_BAD_REQUEST)


class UserBookingHistoryAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user)
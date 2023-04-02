from rest_framework import serializers

from Apartment.models import Apartment
from users.models import CustomUser
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    apartment = serializers.SlugRelatedField(slug_field='street', queryset=Apartment.objects.all())
    check_in = serializers.DateField(required=True)
    check_out = serializers.DateField(required=True)

    class Meta:
        model = Booking
        fields = ['apartment', 'user', 'check_in', 'check_out', 'is_confirmed']
        read_only_fields = ['user', 'is_confirmed']

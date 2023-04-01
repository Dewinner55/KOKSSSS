from rest_framework import serializers

from Apartment.models import Apartment
from users.models import CustomUser
from .models import ApartmentsRating


class RatingSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    apartment = serializers.CharField(max_length=200, required=False)
    apartment_id = serializers.CharField(max_length=200)

    class Meta:
        model = ApartmentsRating
        fields = ('id', 'apartment', 'user', 'rating', 'created_at', 'apartment_id')

    # def create(self, validated_data):
    #     apartment_id = validated_data.pop('apartment', None)
    #     if apartment_id is not None:
    #         validated_data['apartment'] = Apartment.objects.get(id=apartment_id)
    #     return super().create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     apartment_id = validated_data.pop('apartment', None)
    #     if apartment_id is not None:
    #         validated_data['apartment'] = Apartment.objects.get(id=apartment_id)
    #     return super().update(instance, validated_data)
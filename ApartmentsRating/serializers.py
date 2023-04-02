from rest_framework import serializers
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
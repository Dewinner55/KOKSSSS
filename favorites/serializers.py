from rest_framework import serializers

from users.models import CustomUser
from .models import Favorites
from Apartment.models import Apartment

class FavoritesSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    apartment = serializers.PrimaryKeyRelatedField(queryset=Apartment.objects.all())
    is_favorite = serializers.BooleanField(default=True)
    street = serializers.SerializerMethodField()

    class Meta:
        model = Favorites
        fields = '__all__'

    def get_street(self, obj):
        return obj.apartment.street

    def validate_is_favorite(self, value):
        if value not in [True, False]:
            raise serializers.ValidationError("is_favorite должен быть равен True или False")
        return value



from django.db.models import Avg
from rest_framework import serializers

from users.models import CustomUser
from .models import Apartment


from django.core.exceptions import ValidationError


class ApartmentSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    images = serializers.ImageField(max_length=None, use_url=True)
    # id = read_only_fields()
    # user = serializers.CharField(max_length=200)

    class Meta:
        model = Apartment
        fields = ('id',
                  'user',
                  'street',
                  'city',
                  'state',
                  'rooms',
                  'number_of_beds',
                  'floor',
                  'category',
                  'price',
                  'description',
                  'images',
                  'zip_code',
                  'comfort',
                  'average_rating')
        extra_kwargs = {
            'street': {'required': True},
            'city': {'required': True},
            'state': {'required': False},
            'rooms': {'required': True},
            'number_of_beds': {'required': True},
            'floor': {'required': True},
            'category': {'required': True},
            'price': {'required': True},
            'description': {'required': False},
            'images': {'required': False},
            'zip_code': {'required': False},
        }

        read_only_fields = ['id']

    def get_average_rating(self, obj):
        average_rating = obj.apartmentsrating_set.aggregate(Avg('rating'))['rating__avg']
        return round(average_rating, 2) if average_rating is not None else None



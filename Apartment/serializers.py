from django.db.models import Avg
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from comment.models import Comment
from users.models import CustomUser
from .models import Apartment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at']
        read_only_fields = ['user', 'created_at']
        ref_name = 'ApartmentCommentSerializer'

class ApartmentSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    comments = CommentSerializer(source='comment_set', many=True, read_only=True)

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
                  'average_rating',
                  'comments',
                  'is_author',
                  'recommend',)
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
            'is_author': {'required': False},
            'recommend': {'required': True},
        }

        read_only_fields = ['id', 'recommend', 'comment']

    def get_average_rating(self, obj):
        average_rating = obj.apartmentsrating_set.aggregate(Avg('rating'))['rating__avg']
        return round(average_rating, 2) if average_rating is not None else None

class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'




from rest_framework import serializers

from comment.models import Comment
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    comment_text = serializers.StringRelatedField(source='comment.text', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'comment', 'comment_text']
        read_only_fields = ['user', ]
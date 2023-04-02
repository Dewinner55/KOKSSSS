from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'apartment', 'user', 'text', 'created_at']
        read_only_fields = ['user', 'created_at']
        ref_name = 'CommentSerializer'

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from like.models import Like
from like.serializers import LikeSerializer


class LikeListAPIView(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

class LikeCreateAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError({"error": "Аутентификация требуется для создания комментариев."},
                                  code=status.HTTP_401_UNAUTHORIZED)

        user = self.request.user
        comment_id = self.request.data.get('comment')

        existing_like = Like.objects.filter(user=user, comment_id=comment_id).first()
        if existing_like is not None:
            raise ValidationError({"Сообщение": "Вы уже поставили лайк на этот комментарий."})

        serializer.save(user=user)

    from django.core.exceptions import PermissionDenied

class LikeDestroyAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def delete(self, request, *args, **kwargs):
        comment_id = request.data.get('comment', None)
        if comment_id is not None:
            like = Like.objects.filter(comment_id=comment_id).first()
            if like:
                if request.user == like.user or request.user.is_staff or request.user.is_superuser:
                    like_id = like.id
                    like_author = like.user.username
                    like.delete()
                    return Response({"success": f"Лайк ID {like_id} пользователя {like_author} удален."},
                                    status=status.HTTP_204_NO_CONTENT)
                else:
                    raise PermissionDenied({"error": "У вас нет прав на удаление этого лайка."})
            else:
                raise ValidationError({"error": "Лайк не найден."})
        else:
            raise ValidationError({"error": "Необходимо указать идентификатор комментария."})

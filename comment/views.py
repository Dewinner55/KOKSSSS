from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment
from .serializers import CommentSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
   # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all()
        apartment_id = self.request.query_params.get('apartment_id', None)

        if apartment_id is not None:
            queryset = queryset.filter(apartment_id=apartment_id)

        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise ValidationError({"error": "Аутентификация требуется для создания комментариев."},
                                  code=status.HTTP_401_UNAUTHORIZED)


class CommentRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user == request.user or request.user.is_staff or request.user.is_superuser:
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError({"error": "Вы можете удалить только свои комментарии или комментарии, если вы являетесь сотрудником или суперпользователем."})

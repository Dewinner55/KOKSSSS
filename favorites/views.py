from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Apartment.models import Apartment
from .models import Favorites
from .serializers import FavoritesSerializer

from django.views.decorators.cache import cache_page


class FavoritesList(generics.ListCreateAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]

    @cache_page(60 * 5)  # кэш на 5 минут
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username
        apartment_id = int(request.data.get('apartment'))

        favorites = Favorites.objects.filter(user=request.user, apartment_id=apartment_id).first()
        if favorites:
            serializer = self.serializer_class(favorites, data=data)
        else:
            serializer = self.serializer_class(data=data)

        serializer.is_valid(raise_exception=True)
        favorites = serializer.save(apartment_id=apartment_id, user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(FavoritesSerializer(favorites).data, status=status.HTTP_201_CREATED, headers=headers)


class FavoritesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]

    @cache_page(60 * 5)  # кэш на 5 минут
    def delete(self, request, *args, **kwargs):
        favorite = self.get_object()
        user = request.user
        if favorite.user == user or user.is_superuser:
            favorite.delete()
            return Response({"Сообщение": "Избранное успешно удалено.", "Пользователь, кто удалил": user.username}, status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied("Вы не являетесь владельцем этого избранного")

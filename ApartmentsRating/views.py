from django.http import Http404
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Apartment.models import Apartment
from users.models import CustomUser
from .models import ApartmentsRating
from .serializers import RatingSerializer

from django.views.decorators.cache import cache_page

from rest_framework import generics


class ApartmentsRatingList(APIView):
    permission_classes = [IsAuthenticated]

    @cache_page(60 * 5)  # кэш на 5 минут
    def get(self, request):
        apartments_ratings = ApartmentsRating.objects.all()
        serializer = RatingSerializer(apartments_ratings, many=True)
        return Response(serializer.data)

    @cache_page(60 * 5)  # кэш на 5 минут
    def post(self, request):
            apartment_id = request.data.get('apartment_id')
            rating_value = request.data.get('rating')

            if apartment_id and rating_value:
                try:
                    rating_data = {
                        'apartment_id': apartment_id,
                        'user': request.user.username,
                        'rating': rating_value
                    }
                    serializer = RatingSerializer(data=rating_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except CustomUser.DoesNotExist:
                    return Response({'error': 'Пользователь с таким username не найден.'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'error': 'Необходимо указать apartment_id и rating.'},
                            status=status.HTTP_400_BAD_REQUEST)


class ApartmentsRatingDetail(APIView):
    permission_classes = [IsAuthenticated]

    @cache_page(60 * 5)  # кэш на 5 минут
    def get_object(self, pk):
        try:
            return ApartmentsRating.objects.get(pk=pk)
        except ApartmentsRating.DoesNotExist:
            raise Http404

    @cache_page(60 * 5)  # кэш на 5 минут
    def get(self, request, pk):
        apartments_rating = self.get_object(pk)
        serializer = RatingSerializer(apartments_rating)
        return Response(serializer.data)

    @cache_page(60 * 5)  # кэш на 5 минут
    def put(self, request, pk):
        apartments_rating = self.get_object(pk)

        # Проверка, является ли пользователь автором оценки или суперюзером
        if request.user != apartments_rating.user and not request.user.is_superuser:
            return Response({'error': 'Вы можете редактировать только свои оценки.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = RatingSerializer(apartments_rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @cache_page(60 * 5)  # кэш на 5 минут
    def delete(self, request, pk):
        apartments_rating = self.get_object(pk)

        # Проверка, является ли пользователь автором оценки или суперюзером
        if request.user != apartments_rating.user and not request.user.is_superuser:
            return Response({'error': 'Вы можете редактировать только свои оценки.'},
                            status=status.HTTP_403_FORBIDDEN)

        apartments_rating.delete()
        return Response({"Сообщение": "Вы успешно удалили.", "ID_Оценка": pk}, status=status.HTTP_204_NO_CONTENT)

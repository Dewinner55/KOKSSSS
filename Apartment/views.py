from rest_framework.response import Response
from rest_framework import generics, status

# from users.models import CustomUser
from .models import Apartment, ApartmentPermission
from .serializers import ApartmentSerializer


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.views.decorators.cache import cache_page

class ApartmentList(generics.ListCreateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    #
    @cache_page(60 * 5)  # кэш на 5 минут
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'street': openapi.Schema(type=openapi.TYPE_STRING, description='Название улицы'),
            'city': openapi.Schema(type=openapi.TYPE_STRING, description='Название города'),
            'state': openapi.Schema(type=openapi.TYPE_STRING, description='Название округа'),
            'rooms': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество комнат'),
            'number_of_beds': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество спальных мест'),
            'floor': openapi.Schema(type=openapi.TYPE_INTEGER, description='Этаж'),
            'category': openapi.Schema(type=openapi.TYPE_STRING, description='Категория жилья'),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Цена'),
            # 'comfort': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Список удобств'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание'),
            'zip_code': openapi.Schema(type=openapi.TYPE_STRING, description='Почтовый индекс'),
        }
    ))
    @cache_page(60 * 5)  # кэш на 5 минут
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        apartment = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(ApartmentSerializer(apartment).data, status=status.HTTP_201_CREATED, headers=headers)


class ApartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @cache_page(60 * 5)  # кэш на 5 минут
    def put(self, request, *args, **kwargs):
        apartment = self.get_object()
        user = request.user
        if user.is_superuser or apartment.user == user:
            serializer = self.serializer_class(apartment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied("Вы не являетесь автором этой квартиры")

    @cache_page(60 * 5)  # кэш на 5 минут
    def delete(self, request, *args, **kwargs):
        apartment = self.get_object()
        user = request.user
        print(apartment.id)
        if user.is_superuser or apartment.user == user:
            apartment.delete()
            return Response({"Сообщение": "Вы успешно удалили.", "Пользователь кто удалил": user.username, "Что удалил": (apartment.street, apartment.city, apartment.state)}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Вы не являетесь автором этой квартиры"}, status=status.HTTP_403_FORBIDDEN)
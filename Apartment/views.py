
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Apartment
from .serializers import ApartmentSerializer, MyPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .tasks import send_email_task



class ApartmentList(generics.ListCreateAPIView):
    pagination_class = MyPagination

    queryset = Apartment.objects.all().order_by('-recommend', 'id')
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['user__username', 'street', 'city', 'state', 'rooms', 'number_of_beds', 'floor', 'category', 'price', 'description' ]
    # filterset_fields = {
    #     'user__username': ['exact'],  # фильтр для user__username
    #     'street': ['exact', 'icontains'],
    #     'city': ['exact', 'icontains'],
    #     'state': ['exact', 'icontains'],
    #     'rooms': ['exact', 'gte', 'lte'],
    #     'number_of_beds': ['exact', 'gte', 'lte'],
    #     'floor': ['exact', 'gte', 'lte'],
    #     'category': ['exact', 'icontains'],
    #     'price': ['exact', 'gte', 'lte'],
    #     'description': ['exact', 'icontains'],
    #     'zip_code': ['exact', 'icontains']
    # }

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        apartment = serializer.save()
        headers = self.get_success_headers(serializer.data)

        subject = "Новая квартира добавлена"
        message = f"Новая квартира была добавлена: {apartment.street}, {apartment.city}"
        from_email = "evelbrus55@gmail.com"
        recipient_list = [request.user.email]

        send_email_task.delay(subject, message, from_email, recipient_list)

        return Response(ApartmentSerializer(apartment).data, status=status.HTTP_201_CREATED, headers=headers)


class ApartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    pagination_class = MyPagination

    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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

    def delete(self, request, *args, **kwargs):
        apartment = self.get_object()
        user = request.user
        print(apartment.id)
        if user.is_superuser or apartment.user == user:
            apartment.delete()
            return Response({"Сообщение": "Вы успешно удалили.", "Пользователь кто удалил": user.username, "Что удалил": (apartment.street, apartment.city, apartment.state)}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Вы не являетесь автором этой квартиры"}, status=status.HTTP_403_FORBIDDEN)
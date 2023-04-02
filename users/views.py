import uuid

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions

from rest_framework.generics import GenericAPIView, ListAPIView

from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

import users.models
from Apartment.serializers import MyPagination
from rest_framework.exceptions import ValidationError
from users import serializers
from .send_mail import send_confirmation_email, send_password_reset_email

from django.contrib.auth import get_user_model

from rest_framework import status, generics
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.response import Response
import logging
# from .serializers import LogoutSerializer

# from .serializers import LogoutSerializer

from django.views.decorators.cache import cache_page
from .serializers import RefreshTokenSerializer

from rest_framework.filters import SearchFilter

from .models import PasswordResetToken
from .models import CustomUser

from django.shortcuts import get_object_or_404
from .serializers import ResendConfirmationCodeSerializer

from .tasks import send_email_task


User = get_user_model()

class RegistrationView(APIView):
    pagination_class = MyPagination

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RegistrationSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_confirmation_email(user.email, user.activation_code)
            except User.DoesNotExist:
                return Response({'Сообщение': 'Некие проблемы с почтой!', 'data': serializer.data}, status=201)
        return Response(serializer.data, status=201)


class ActivationView(GenericAPIView):
    pagination_class = MyPagination

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ActivationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Ваш аккаунт успешно активирован!', status=200)


class ResendConfirmationCodeView(APIView):
    def post(self, request):
        serializer = ResendConfirmationCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)

        if user.is_active:
            return Response({'Ошибка': 'Пользователь уже активирован'}, status=status.HTTP_400_BAD_REQUEST)

        send_confirmation_email(user.email, user.activation_code)
        return Response({'Сообщение': 'Код активации отправлен.'}, status=status.HTTP_200_OK)

class LoginView(TokenObtainPairView):
    pagination_class = MyPagination

    permission_classes = (permissions.AllowAny,)


class UserListApiView(ListAPIView):
    pagination_class = MyPagination


    queryset = User.objects.all().order_by('id')
    serializer_class = serializers.UserSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['username', 'email']
    filterset_fields = {
        'username': ['exact'],  # фильтр для user__username
    }



class LogoutView(generics.GenericAPIView):

    pagination_class = MyPagination

    serializer_class = RefreshTokenSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            serializer.save()
            return Response({"Сообщение": "Вы успешно вышли из системы.", "Пользователь": user.username}, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


logger = logging.getLogger(__name__)


class MyView(APIView):

    pagination_class = MyPagination

    @cache_page(60 * 5)  # кэш на 5 минут
    def get(self, request):
        logger.debug('Debug message')
        logger.info('Info message')
        logger.warning('Warning message')
        logger.error('Error message')
        logger.critical('Critical message')
        return Response({'message': 'Hello, world!'})


class PasswordResetRequestView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'Сообщение': 'Пользователь с указанным адресом электронной почты не найден.'}, status=status.HTTP_404_NOT_FOUND)

        reset_token = str(uuid.uuid4())
        PasswordResetToken.objects.create(user=user, token=reset_token)

        send_password_reset_email(user.email, reset_token)

        return Response({'Сообщение': 'Письмо со ссылкой для сброса пароля отправлено.'}, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        password = serializer.validated_data['password']
        password2 = serializer.validated_data['password2']

        if password != password2:
            return Response({'password': 'Пароли должны совпадать.'})

        try:
            reset_token = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response({'Сообщение': 'Недействительный токен сброса пароля.'}, status=status.HTTP_400_BAD_REQUEST)

        if reset_token.is_expired():
            return Response({'Сообщение': 'Токен сброса пароля истек.'}, status=status.HTTP_400_BAD_REQUEST)

        user = reset_token.user
        user.set_password(password)
        user.save()

        reset_token.delete()

        return Response({'Сообщение': 'Пароль успешно сброшен и обновлен.'}, status=status.HTTP_200_OK)
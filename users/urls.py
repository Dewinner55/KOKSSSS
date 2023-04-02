from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import LogoutView, MyView, LoginView

urlpatterns = [
    # ...
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/', views.ActivationView.as_view()),
    path('activate-refresh/', views.ResendConfirmationCodeView.as_view()),
    path('login/', views.LoginView.as_view(), name='login'),
    path('users/', views.UserListApiView.as_view(), name='users'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my_view/', MyView.as_view(), name='my_view'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('password_reset_request/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),

    # ...
]

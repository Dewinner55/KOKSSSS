from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import LogoutView, MyView

urlpatterns = [
    # ...
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/', views.ActivationView.as_view()),
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.UserListApiView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my_view/', MyView.as_view(), name='my_view'),


    # ...
]

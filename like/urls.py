from django.urls import path

from . import views
from .views import LikeListAPIView

urlpatterns = [
    # другие маршруты
    path('likes/', LikeListAPIView.as_view(), name='like-list'),
    path('likes-create/', views.LikeCreateAPIView.as_view(), name='likes'),
    path('likes-delete/', views.LikeDestroyAPIView.as_view(), name='likes')
]

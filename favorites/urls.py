from django.urls import path
from .views import FavoritesList, FavoritesDetail

urlpatterns = [
    path('favorites/', FavoritesList.as_view()),
    path('favorites/<int:pk>/', FavoritesDetail.as_view()),
]
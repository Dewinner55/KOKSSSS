from django.urls import path
from .views import ApartmentsRatingList, ApartmentsRatingDetail

urlpatterns = [
    path('apartments-ratings/', ApartmentsRatingList.as_view()),
    path('apartments-ratings/<int:pk>/', ApartmentsRatingDetail.as_view()),

]
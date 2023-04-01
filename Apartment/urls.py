from django.urls import path
from .views import ApartmentList, ApartmentDetail

urlpatterns = [
    path('apartments/', ApartmentList.as_view()),
    path('apartments/<int:pk>/', ApartmentDetail.as_view()),
]
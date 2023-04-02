from django.urls import path

from . import views

urlpatterns = [
    # другие маршруты
    path('comments/', views.CommentListCreateAPIView.as_view(), name='comments'),
    path('comments/<int:pk>/', views.CommentRetrieveDestroyAPIView.as_view(), name='comment-detail'),

]
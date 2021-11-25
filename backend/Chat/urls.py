from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:pk>/', views.ChatView.as_view()),
    path('chat/', views.ChatView.as_view()),
]
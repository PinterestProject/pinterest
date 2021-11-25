from django.urls import path
from . import views

urlpatterns = [
    path('favourite/<int:pk>/', views.FavouriteView.as_view()),
    path('favourite/', views.FavouriteView.as_view()),
]
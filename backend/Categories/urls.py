from django.conf.urls import url, include
from django.urls import path
from .views import categoriesList,categoriesCreate,categoryDelete, categoryUpdate



urlpatterns = [
    path('',categoriesList, name='categories-list'),
    path('create',categoriesCreate , name='categories-create'),
    path('delete/<int:pk>', categoryDelete, name='categories-delete'),
    path('update/<int:pk>',categoryUpdate, name='categories-update')

]
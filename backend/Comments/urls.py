from django.urls import path , include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

urlpatterns = [

    path('comment/list',comment_list.as_view()), #get comments list
    path('comment/',comment_api.as_view()), #create comment
    path('comment/<int:pk>',comment_api.as_view()), #delete,patch,get comment
    path('like',like_api.as_view()), #create Like
    path('like/<int:pk>',like_api.as_view()), #delete,get
    path('likes/<int:pk>',likes_for_comment.as_view()), #gel all likes for a comment bt enter the pk of a comment
    path('reply',reply_api.as_view()), #create Like
    path('reply/<int:pk>',reply_api.as_view()), #delete,get
    path('replies/<int:pk>',replies_for_comment.as_view()) #get all comments by enter the pk of a comment

    ]

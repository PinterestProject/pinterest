from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth.models import User
#
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
#
from . import views

router=DefaultRouter()

router.register('users',views.UserViewSet,basename='users')
# router.register('users',views.signup,basename='users')

urlpatterns=[
    path('',include(router.urls)),
    path('signup/',views.UserRegisterHandler.signup),
    path('logout/',views.UserRegisterHandler.logout),
    path('login/',obtain_auth_token),
    path('changepassword/<str:old_password>',views.UserChangePasswordHandler.change_password)
]

from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth.models import User
#
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
#
from . import views

# from views import UserٍSendInvitation, invitation_create

from .views import relationList, relationDelete,followedsList, followersList


router=DefaultRouter()

router.register('users',views.UserViewSet,basename='users')
router.register('follow',views.RelationshipViewSet,basename='follow')
# router.register('users',views.signup,basename='users')
# router.register('invitation',views,basename='invitation')


urlpatterns=[
    path('',include(router.urls)),
    path('signup/',views.UserRegisterHandler.signup),
    path('logout/',views.UserRegisterHandler.logout),
    path('login/',obtain_auth_token),
    path('changepassword/',views.UserChangePasswordHandler.change_password),
    path('user-details/',views.UserRegisterHandler.profile_data),
    path('board/invite/', views.InvitationList.as_view(), name="create-invite"),

    # path('board/invite',views.invitation_create, name="create-invite"),
    # path('board/invite/<int:pk>',views.get_invitation, name="get-invite"),


    path('relation/list',relationList),
    path('relation/delete', relationDelete),
    path('relation/followed/<int:pk>',followedsList),
    path('relation/follower/<int:pk>',followersList),

]


from django.shortcuts import render
from django.contrib.auth import get_user_model
#
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
#
from rest_framework import status
from rest_framework import serializers
#
from .serializers import UserSerializer, InvitationSerializer
#
from .models import User, Invitation
# Create your views here.
# User=get_user_model()




class UserViewSet(ModelViewSet):
    """
    usage of this class with be in the following cases
    1- retrieve all users accounts
    2- update any profile
    3- delete auy profile
    4- it can be use to signup also but no login no logout no tokens
    just normal CRUD operations on User model
    important : never try to change password from here because it'll stored plain not hashed
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def create(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response({'message':user.data})
        return Response({'message':user.errors})
    # def create(self, request, *args, **kwargs):
    #
    #     if request.data['password']!= request.data['password_conf']:
    #         raise serializers.ValidationError({'password':'confirmed password did not match'})
    #     else :
    #         user = User(email=request.data['email'],username=request.data['username'])
    #         user_serialized=UserSerializer(instance=user,data=request.data)
    #         user.set_password(request.data['password'])
    #         if user_serialized.is_valid():
    #             # print(user.instance)
    #             user.save()
    #             return Response({'message':user_serialized.data})
    #         else:
    #             return Response({'message':user_serialized.errors})
            # return Response({"message":status.HTTP_406_NOT_ACCEPTABLE})

class UserRegisterHandler():
    @api_view(['POST'])
    def signup(request):
        # if request.data['password'] != request.data['password_conf']:
        #     raise serializers.ValidationError({'password': 'confirmed password did not match'})
        # else:
        user = UserSerializer(data=request.data)
        if user.is_valid():
            # print(user.instance)
            user.save()
            created_user=User.objects.get(email=user.data['email'])
            token=Token.objects.create(user=created_user)
            return Response({'user_token':token.key})
        return Response({'message':user.errors})

    @api_view(['POST'])
    def logout(request):
        username=request.user.username
        request.user.auth_token.delete()
        return Response({"message":f"bye bye {username}"})


class UserChangePasswordHandler():
    @api_view(['POST'])
    def change_password(request,old_password):
        # print("user id =>",request.user.id)
        # print("1st check equality =>",User.objects.get(pk=request.user.id).check_password(old_password))
        # print("old sent password =>",old_password)
        # print("1st check equality =>",request.user.check_password(request.data['old_pass']))
        if request.user.check_password(request.data['old_pass']) :
            request.user.set_password(request.data['new_password'])
            request.user.save()
            return Response({"message":"password updated!"})
        return Response({"message ":request.user.check_password(request.data['old_pass'])})



class InvitationList(APIView):
    """
    List all boards, or create a new board.
    """

    def get(self, request, format=None):
        boards = Invitation.objects.all()
        serialized_invitations = InvitationSerializer(instance=boards, many=True)
        return Response(data=serialized_invitations.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serialized_invitations = InvitationSerializer(data=request.data)
        if serialized_invitations.is_valid():
            serialized_invitations.save()
            return Response(serialized_invitations.data, status=status.HTTP_201_CREATED)
        return Response(serialized_invitations.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# def invitation_create(request):
#     serialized_invitation = InvitationSerializer(data=request.data)
#     if serialized_invitation.is_valid():
#         serialized_invitation.save()
#     else:
#         return Response(data=serialized_invitation.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def get_invitation(request,pk):
#     try:
#         invitation = Invitation.objects.get(pk=pk)

#     except Exception as e:
#         return Response(data={'message':'failed Invite dose not exist'}, status=status.HTTP_400_BAD_REQUEST)

#     serialized_invitation = InvitationSerializer(instance=invitation)
#     return Response(data=serialized_invitation.data, status=status.HTTP_200_OK)

# class UserٍSendInvitation(BasePermission):

#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             return True
#         return False

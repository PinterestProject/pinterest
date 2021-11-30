from django.shortcuts import render
from django.contrib.auth import get_user_model
#
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

#
from rest_framework import status
from rest_framework import serializers
#

from .serializers import UserSerializer, InvitationSerializer
#
from .models import User, Invitation
# Create your views here.
# User=get_user_model()

from .serializers import relationSerializer

from .serializers import RelationSerializer
from .models import Relationship
from .permissions import UserPermissions

# Create your views here.
User=get_user_model()

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
    permission_classes = [UserPermissions]
    # authentication_classes = [TokenAuthentication]


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


    def partial_update(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        self.check_object_permissions(request,user)
        user_serialized = UserSerializer(instance=user,data=request.data,partial=True)

        if user_serialized.is_valid():
            user_serialized.update(instance=user,validated_data=request.data)
            return Response({"message":user_serialized.data})
        return Response({'message':user_serialized.errors})

    def update(self, request, *args, **kwargs):
        """
        handle full user update
        """
        user = User.objects.get(pk=kwargs['pk'])
        self.check_object_permissions(request=request,obj=user)
        user_serialized = UserSerializer(instance=user,data=request.data)
        if user_serialized.is_valid():
            user_serialized.update(instance=user,validated_data=request.data)
            return Response({"message":user_serialized.data})
        return Response({'message':user_serialized.errors})



class UserRegisterHandler():
    @api_view(['POST'])
    def signup(request):

        # if request.data['password'] != request.data['password_conf']:
        #     raise serializers.ValidationError({'password': 'confirmed password did not match'})
        # else:

        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            created_user=User.objects.get(email=user.data['email'])
            token=Token.objects.create(user=created_user)
            return Response({'user_token':token.key},status=status.HTTP_201_CREATED)
        return Response({'message':user.errors},status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    def logout(request):
        username=request.user.username
        request.user.auth_token.delete()
        return Response({"message":f"bye bye {username}"})


class UserChangePasswordHandler():
    @api_view(['POST'])
    def change_password(request):

        if request.user.check_password(request.data['old_pass']) :
            request.user.set_password(request.data['new_password'])
            request.user.save()
            return Response({"message":"password updated!"},status=status.HTTP_200_OK)
        return Response({"message ":request.usercheck_password(request.data['old_pass'])},status=status.HTTP_400_BAD_REQUEST)



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


## relationship views ##

@api_view(['GET'])
def relationList(request):
    rel = Relationship.objects.all()
    serialized_rel = relationSerializer(instance=rel, many=True)
    return Response(data=serialized_rel.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def relationDelete(request, pk):
    response = {}
    try:
        rel_obj = Relationship.objects.get(pk=pk)
        rel_obj.delete()
        response['data'] = {'message': 'successfully Deleted'}
        response['status'] = status.HTTP_200_OK
    except Exception as e:
        response['data'] = {'message': 'ERROR:While Deleting movie'}
        response['status'] = status.HTTP_400_BAD_REQUEST
    return Response(**response)

@api_view(['GET'])
def followedsList(request,pk):
    res={}
    rel_list= Relationship.objects.all()
    serialized_rel = relationSerializer(instance=rel_list, many=True)
    flist = serialized_rel.data
    filter_result = filter(lambda d: d.get('follower_id') == pk, flist)
    finalList=list(filter_result)
    res['followeds']= finalList
    res['count'] = {len(finalList)}
    return Response(res)


@api_view(['GET'])
def followersList(request,pk):
    res={}
    rel_list = Relationship.objects.all()
    serialized_rel = relationSerializer(instance=rel_list, many=True)
    flist = serialized_rel.data
    filter_result = filter(lambda d: d.get('followed_id') == pk, flist)
    finalList = list(filter_result)
    res['followers'] = finalList
    res['count'] = {len(finalList)}
    return Response(res)

class RelationshipViewSet(ModelViewSet):
     serializer_class = RelationSerializer
     queryset = Relationship.objects.all()

     def create(self, request, *args, **kwargs):
         print(request.data)
         request.data['follower_id']=request.user.id
         relation=RelationSerializer(data=request.data)
         if relation.is_valid():
             relation.save()
             return Response({'message':status.HTTP_201_CREATED})
         return Response({'message':status.HTTP_400_BAD_REQUEST})

# class UserFollowing():
#     @api_view(['GET'])
#     def who_user_follow(self):
#         user=self.user
#         stars=user.following.all()
#         # fans=user.following.all()
#         return Response({'accounts':UserSerializer(instance=starts,many=True).data})
#     @api_view(['GET'])
#     def who_follow_user(self):
#         user=self.user
#         # fans=user.followers.all()
#         fans=user.followers.all()
#         return Response({'accounts':UserSerializer(instance=fans,many=True).data})



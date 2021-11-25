from django.shortcuts import render
from django.contrib.auth import get_user_model
#
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
#
from rest_framework import status
from rest_framework import serializers
#

from .serializers import UserSerializer,relationSerializer


# from .serializers import RelationSerializer
from .models import User
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
        user = UserSerializer(data=request.data)
        if user.is_valid():
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
        if request.user.check_password(request.data['old_pass']) :
            request.user.set_password(request.data['new_password'])
            request.user.save()
            return Response({"message":"password updated!"})
        return Response({"message ":request.user.check_password(request.data['old_pass'])})




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

# class RelationshipViewSet(ModelViewSet):
#     serializer_class = RelationSerializer
#     queryset = Relationship.objects.all()

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


from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *



class comment_api(APIView):


    def get(self,request,pk, *args,**kwargs):
        response = {}
        comment = comments.objects.filter(pin_id=pk)
        users=[{"id":i.user_id.id,"username":i.user_id.username} for i in comment]
        serializer = CommentSerializer(instance=comment,many=True)
        response['data'] = {'data':serializer.data,'users':users}
        response['status'] = status.HTTP_200_OK
        return Response(**response)


    def post(self,request, *args,**kwargs):
        request.data['user_id']=request.user.id
        serializers = CommentSerializer(data=request.data)
        # print(serializers)
        if serializers.is_valid():
            print("serializers")
            serializers.save()
            return Response({'message': serializers.data})
        return Response({'message': serializers.errors})
    def delete (self,request,pk,*args,**kwargs):
        response = {}
        try:
            like = comments_likes.objects.get(pk=pk)
            like.delete()
            response['data'] = {'message': 'Successfully Deleted the comment'}
            response['status'] = status.HTTP_200_OK
        except Exception as e:
            response['data'] = {'message': 'Error While Deleting comment -- {} -- Target Comment{}'.format(str(e), pk)}
            response['status'] = status.HTTP_400_BAD_REQUEST

        print("Result -> ", response)
        return Response(**response)

    def patch(self, request, pk, *args, **kwargs):
        try:
            comment = comments.objects.get(pk=pk)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


        serialize= CommentSerializer(instance=comment, data=request.data, partial=True)

        if serialize.is_valid():
            serialize.save()
            return Response(data=serialize.data, status=status.HTTP_200_OK)

        return Response(data=serialize.errors, status=status.HTTP_400_BAD_REQUEST)


class comment_list(APIView):

    def get(self, request, *args,**kwargs):
        comment = comments.objects.all()
        serializer = CommentSerializer(instance=comment, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



class like_api(APIView):

    def get(self,request,pk, *args,**kwargs):
        response = {}
        like = comments_likes.objects.filter(pk=pk)
        if like.exists():
            like = like.first()
            serializer = LikeSerializer(instance=like)

            response['data'] = serializer.data
            response['status'] = status.HTTP_200_OK
        else:
            response['data'] = {'message': 'failed Comment like does not exist'}
            response['status'] = status.HTTP_400_BAD_REQUEST

        return Response(**response)



    def post(self,request, *args,**kwargs):
        serializers = LikeSerializer(data=request.data,many=True)
        if serializers.is_valid():
            serializers.save()
            return Response({'message': serializers.data})
        return Response({'message': serializers.errors})

    def delete (self,request,pk,*args,**kwargs):
        response = {}
        try:
            like = comments_likes.objects.get(pk=pk)
            like.delete()
            response['data'] = {'message': 'Successfully Deleted the comment'}
            response['status'] = status.HTTP_200_OK
        except Exception as e:
            response['data'] = {'message': 'Error While Deleting like -- {} -- Target Comment_like {}'.format(str(e), pk)}
            response['status'] = status.HTTP_400_BAD_REQUEST

        print("Result -> ", response)
        return Response(**response)

class likes_for_comment(APIView):

    def get(self, request, pk,*args,**kwargs):
        try:
            comment = comments.objects.get(pk=pk)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            like = comments_likes.objects.filter(comment_id=comment.id)
            serializer = LikeSerializer(instance=like,many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class reply_api(APIView):


    def get(self,request,pk, *args,**kwargs):
        response = {}
        reply = comment_reply.objects.filter(pk=pk)
        if reply.exists():
            reply = reply.first()
            serializer = CommentSerializer(instance=reply)

            response['data'] = serializer.data
            response['status'] = status.HTTP_200_OK
        else:
            response['data'] = {'message': 'failed Comment Reply does not exist'}
            response['status'] = status.HTTP_400_BAD_REQUEST

        return Response(**response)


    def post(self,request, *args,**kwargs):
        serializer = ReplySerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data})
        return Response({'message': serializer.errors})

    def delete (self,request,pk,*args,**kwargs):
        response = {}
        try:
            reply = comment_reply.objects.get(pk=pk)
            reply.delete()
            response['data'] = {'message': 'Successfully Deleted the comment reply'}
            response['status'] = status.HTTP_200_OK
        except Exception as e:
            response['data'] = {'message': 'Error While Deleting reply -- {} -- Target reply {}'.format(str(e), pk)}
            response['status'] = status.HTTP_400_BAD_REQUEST

        print("Result -> ", response)
        return Response(**response)

    def patch(self, request, pk, *args, **kwargs):
        try:
            reply = comment_reply.objects.get(pk=pk)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serialize= ReplySerializer(instance=reply, data=request.data, partial=True)

        if serialize.is_valid():
            serialize.save()
            return Response(data=serialize.data, status=status.HTTP_200_OK)

        return Response(data=serialize.errors, status=status.HTTP_400_BAD_REQUEST)


class replies_for_comment(APIView):

    def get(self, request, pk,*args,**kwargs):
        try:
            comment = comments.objects.get(pk=pk)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            reply = reply_api.objects.filter(comment_id=comment.id)
            serializer = ReplySerializer(instance=reply,many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

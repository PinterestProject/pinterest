from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *



class comment_api(APIView):


    def get(self,request,pk, *args,**kwargs):
        response = {}
        comment = comments.objects.filter(pk=pk)
        if comment.exists():
            comment = comment.first()
            serializer = CommentSerializer(instance=comment)

            response['data'] = serializer.data
            response['status'] = status.HTTP_200_OK
        else:
            response['data'] = {'message': 'failed Comment does not exist'}
            response['status'] = status.HTTP_400_BAD_REQUEST

        return Response(**response)


    def post(self,request, *args,**kwargs):
        serializers = CommentSerializer(data=request.data,many=True)
        print(serializers)
        if serializers.is_valid():
            print(serializers)
            serializers.save()
            return Response({'message': serializers.data})
        return Response({'message': serializers.errors})
    def delete (self,request,pk,*args,**kwargs):
        response = {}
        try:
            comment = comments.objects.get(pk=pk)
            comment.delete()
            response['data'] = {'message': 'Successfully Deleted the comment'}
            response['status'] = status.HTTP_200_OK
        except Exception as e:
            response['data'] = {'message': 'Error While Deleting Movie -- {} -- Target Movie {}'.format(str(e), pk)}
            response['status'] = status.HTTP_400_BAD_REQUEST

        print("Result -> ", response)
        return Response(**response)

    def patch(self, request, pk, *args, **kwargs):
        try:
            comment = comments.objects.get(pk=pk)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # if request.method == 'PUT':
        #     serialized_movie = MovieSerializer(instance=movie, data=request.data)

        serialize= CommentSerializer(instance=comment, data=request.data, partial=True)

        if serialize.is_valid():
            serialize.save()
            return Response(data=serialize.data, status=status.HTTP_200_OK)

        return Response(data=serialize.errors, status=status.HTTP_400_BAD_REQUEST)


class comment_list(APIView):

    def get(self, request, *args,**kwargs):
        movies = comments.objects.all()
        serializer = CommentSerializer(instance=movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

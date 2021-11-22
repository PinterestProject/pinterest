from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer
# Create your views here.

@api_view(['GET'])
def categoriesList(request):
    categories = Category.objects.all()
    serialized_categories = CategorySerializer(instance=categories, many=True)

    return Response(data=serialized_categories.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def categoriesCreate(request):
    serialized_category = CategorySerializer(data=request.data)
    if serialized_category.is_valid():
        serialized_category.save()
    else:
        return Response(data=serialized_category.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=serialized_category.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def categoryDelete(request, pk):
    response = {}
    try:
        category_obj = Category.objects.get(pk=pk)
        category_obj.delete()
        response['data'] = {'message': 'successfully Deleted'}
        response['status'] = status.HTTP_200_OK
    except Exception as e:
        response['data'] = {'message': 'ERROR:While Deleting movie'}
        response['status'] = status.HTTP_400_BAD_REQUEST

    return Response(**response)


@api_view(['PUT', 'PATCH'])
def categoryUpdate(request, pk):
    category = Category.objects.get(pk=pk)

    if request.method == 'PUT':
        serialized_categry = CategorySerializer(instance=category, data=request.data)
    elif request.method == 'PATCH':
        serialized_categry = CategorySerializer (instance=category, data=request.data, partial=True)

    if serialized_categry.is_valid():
        serialized_categry.save()
        return Response(data=serialized_categry.data, status=status.HTTP_200_OK)

    return Response(data=serialized_categry.errors, status=status.HTTP_400_BAD_REQUEST)




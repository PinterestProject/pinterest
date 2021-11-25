from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Favourite
from Users.models import User
from .serializers import FavouriteSerializer


# Create your views here.
class FavouriteView(APIView):

    # get user using user pk
    def get_user(self, pk):
        return User.objects.get(pk=pk)

    # get favourite using favourite pk
    def get_favourite(self, pk):
        return Favourite.objects.get(pk=pk)

    # get user favourites using user pk
    def get(self, request, pk, format=None):
        try:
            user = self.get_user(pk)
            favourites = Favourite.objects.filter( user_id=user.id)
        except Favourite.DoesNotExist:
            return Response("Sorry! Doesn't Exist🙁")
        serializer = FavouriteSerializer(favourites, many=True)
        return Response(serializer.data)

    # adding new favourite, send user pk in the parameters & pin id in the body
    def post(self, request, format=None):
        userpk = request.GET.get('pk')
        user = self.get_user(pk=userpk)
        print(user)
        print(request.data)
        request.data._mutable = True
        request.data.update({'user_id': user.id})
        serializer = FavouriteSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    # deleting favourite, using favourite id
    def delete(self, request, pk, format=None):
        try:
            favourite = self.get_favourite(pk)
        except Favourite.DoesNotExist:
            return Response("Sorry! Doesn't Exist🙁")
        operation = favourite.delete()
        data = {}
        if operation:
            data["sucess"] = "Deleted successfully😘"
        else:
            data["failure"] = "Delete failed😢"
        return Response(data=data)
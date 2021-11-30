from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Pins.models import Pin
from .serializers import PinSerializer
# from Users.models import User


class PinList(APIView):
    """
    List all pins, or create a new pin.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        pins = Pin.objects.all()
        serialized_pins = PinSerializer(instance=pins, many=True)
        return Response(data=serialized_pins.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # use user_id from request data as required pin author user_id
        request.data["user_id"] = request.user.id
        serialized_pin = PinSerializer(data=request.data)
        if serialized_pin.is_valid():
            serialized_pin.save()
            return Response(serialized_pin.data, status=status.HTTP_201_CREATED)
        return Response(serialized_pin.errors, status=status.HTTP_400_BAD_REQUEST)


class PinDetails(APIView):
    """
    Retrieve, update or delete a pin instance.
    """

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Pin.objects.get(pk=pk)
        except Pin.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pin = self.get_object(pk)
        serialized_pin = PinSerializer(pin)
        # print(f"{User.objects.get(id=serialized_pin.data['user_id']).username }")
        return Response(serialized_pin.data)

    def patch(self, request, pk, format=None):
        pin = self.get_object(pk)
        # if and only if user is the pin author
        print(f"{request.user.email = }")
        print(f"{str(pin.user_id) = }")
        # pin.user_id returns the user email instead of user id 🤷‍♂️
        if request.user.email == str(pin.user_id):
            serialized_pin = PinSerializer(pin, data=request.data, partial=True)
            if serialized_pin.is_valid():
                serialized_pin.save()
                return Response(serialized_pin.data)
            return Response(serialized_pin.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk, format=None):
        pin = self.get_object(pk)
        # if and only if user is the pin author
        # pin.user_id returns the user email instead of user id 🤷‍♂️
        if request.user.email == str(pin.user_id):
            serialized_pin = PinSerializer(pin, data=request.data)
            if serialized_pin.is_valid():
                serialized_pin.save()
                return Response(serialized_pin.data)
            return Response(serialized_pin.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        pin = self.get_object(pk)
        # if and only if user is the pin author
        # pin.user_id returns the user email instead of user id 🤷‍♂️
        if request.user.email == str(pin.user_id):
            pin.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.decorators import api_view

@api_view(['GET'])
def get_board_pins(request, pk):
    pins = Pin.objects.filter(boards = pk)
    serialized_pins = PinSerializer(pins, many=True)
    print(f"{len(serialized_pins.data)} = ")
    return Response(data=serialized_pins.data, status=status.HTTP_200_OK)
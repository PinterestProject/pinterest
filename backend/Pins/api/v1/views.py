from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from Pins.models import Pin
from .serializers import PinSerializer


@api_view(["GET"])
def get_pins(request):
    pins = Pin.objects.all()
    serialized_pins = PinSerializer(instance=pins, many=True)

    return Response(data=serialized_pins.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_pin(request):
    serialized_pin = PinSerializer(data=request.data)
    if serialized_pin.is_valid():
        serialized_pin.save()
    else:
        return Response(data=serialized_pin.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=serialized_pin.data, status=status.HTTP_200_OK)

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Boards.api.v1.serializers import BoardSerializer
from Boards.models import Board
from Pins.models import Pin
from .serializers import PinSerializer


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
        # request.data._mutable=True
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_board_pins(request, pk):
    pins = Pin.objects.filter(boards=pk)
    board = Board.objects.get(id=pk)
    serialized_pins = PinSerializer(pins, many=True)
    serialized_board = BoardSerializer(board)
    return Response(
        data=(serialized_board.data, serialized_pins.data), status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_board_pins(request):
    boards = Board.objects.filter(created_by=request.user.id)
    serialized_board = BoardSerializer(boards, many=True)
    print(serialized_board.data, len(serialized_board.data))
    if len(serialized_board.data) > 0:
        board_id = []
        for bo in serialized_board.data:
            board_id.append(bo["id"])
            # pins = Pin.objects.filter(boards=bo["id"])

        pins = Pin.objects.filter(boards__in=board_id)
        serialized_pins = PinSerializer(pins, many=True)
        data = {}
        data["boards"] = serialized_board.data
        data["pins"] = serialized_pins.data
        return Response(data, status=status.HTTP_200_OK)
    return Response(data=(serialized_board.data), status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_pins(request):
    pins = Pin.objects.filter(user_id=request.user.id)
    serialized_pins = PinSerializer(instance=pins, many=True)
    print(f"{len(serialized_pins.data)} = ")
    return Response(data=serialized_pins.data, status=status.HTTP_200_OK)


# filter pin


def catePins(pk):
    returnData = []
    pins = Pin.objects.all()
    serialized_pins = PinSerializer(instance=pins, many=True)

    pin_list = serialized_pins.data

    for pin in pin_list:
        cate_pin = pin["categories"]
        for ele in cate_pin:
            if ele == pk:
                returnData.append(pin)
    return returnData


def Convert(string):
    li = list(string.split(","))
    return li


@api_view(["POST"])
def pinsOfSpecificCategory(request):
    finalPins = []
    data = Convert(request.data["categories"])
    for i in range(len(data)):
        lis = catePins(int(data[i]))
        for x in range(len(lis)):
            finalPins.append(lis[x])
    print(finalPins)
    return Response(finalPins)

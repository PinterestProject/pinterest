from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Boards.models import Board
from .serializers import BoardSerializer


class BoardList(APIView):
    """
    List all boards, or create a new board.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        # print(f"{request.user = }")
        # print(f"{request.user.id = }")
        # get current user boards
        boards = Board.objects.filter(created_by=request.user.id)
        serialized_boards = BoardSerializer(instance=boards, many=True)
        return Response(data=serialized_boards.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # use user id from request data as required board creator id
        # request.data._mutable = True
        request.data["created_by"] = request.user.id
        # request.data._mutable = False
        serialized_board = BoardSerializer(data=request.data)
        if serialized_board.is_valid():
            serialized_board.save()
            return Response(serialized_board.data, status=status.HTTP_201_CREATED)
        return Response(serialized_board.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetails(APIView):
    """
    Retrieve, update or delete a board instance.
    """

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        board = self.get_object(pk)
        serialized_board = BoardSerializer(board)
        return Response(serialized_board.data)

    def patch(self, request, pk, format=None):
        board = self.get_object(pk)
        if request.user.email == str(board.created_by):
            serialized_board = BoardSerializer(board, data=request.data, partial=True)
            if serialized_board.is_valid():
                serialized_board.save()
                return Response(serialized_board.data)
            return Response(serialized_board.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk, format=None):
        board = self.get_object(pk)
        if request.user.email == str(board.created_by):
            serialized_board = BoardSerializer(board, data=request.data)
            if serialized_board.is_valid():
                serialized_board.save()
                return Response(serialized_board.data)
            return Response(serialized_board.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        board = self.get_object(pk)
        if request.user.email == str(board.created_by):
            board.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

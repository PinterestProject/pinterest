from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from Users.models import User
from .models import Chat
from .serializers import ChatSerializer
from rest_framework.response import Response

# Create your views here.

class ChatView(APIView):

    #get user using user pk
    def get_user(self, pk):
            return User.objects.get(pk=pk)

    # get message using message pk
    def get_message(self, pk):
            return Chat.objects.get(pk=pk)

    # get chat between 2 users, reciever pk in the url, sender pk in the parameters
    def get(self, request, pk, format=None):
        try:
            reciever = self.get_user(pk=pk)
            senderpk = request.GET.get('pk')
            sender = self.get_user(pk=senderpk)
            chat = Chat.objects.filter(sender_id=sender.id , receiver_id=reciever.id) | Chat.objects.filter(
                sender_id=reciever.id, receiver_id=sender.id
            )
        except Chat.DoesNotExist:
            return Response("Sorry! Doesn't Exist🙁")
        serializer = ChatSerializer(chat, many=True)
        return Response(serializer.data)

    #post new message pk1 of the sender, pk2 of the reiever and both are send in the parameters
    def post(self, request, format=None):
        recieverpk = request.GET.get('pk2')
        senderpk = request.GET.get('pk1')
        sender = self.get_user(pk=senderpk)
        reciever = self.get_user(pk=recieverpk)
        print(sender)
        print(reciever)
        print(request.data)
        request.data._mutable = True
        request.data.update({"sender_id": sender.id,"receiver_id": reciever.id})
        print(request.data)
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    # delete message in chat using message pk
    def delete(self, request, pk, format=None):
        try:
            message = self.get_message(pk=pk)
        except Chat.DoesNotExist:
            return Response("Sorry! Doesn't Exist🙁")
        operation = message.delete()
        data = {}
        if operation:
            data["sucess"] = "Deleted successfully😘"
        else:
            data["failure"] = "Delete failed😢"
        return Response(data=data)

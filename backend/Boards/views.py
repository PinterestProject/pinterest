from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import permissions
from rest_framework import viewsets
from . import models

class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='board-crud').exists():
            return True
        return False


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False



# class UserCrudonBoard(viewsets.ModelViewSet):

#     permission_classes = [IsStaff | IsOwner] # or operator used

#     queryset = objects.objects.all()
#     serializer_class = MessageSerializer
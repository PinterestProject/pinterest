from rest_framework.permissions import BasePermission
from rest_framework import permissions
class UserPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(obj.email)
        print(request.user.email)
        return True if request.method in permissions.SAFE_METHODS else obj.email == request.user.email

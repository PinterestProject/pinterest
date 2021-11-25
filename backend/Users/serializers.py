from rest_framework import serializers
from rest_framework import status
#
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
#
from django.contrib.auth import get_user_model
#

from .models import User
from .models import Relationship

#
User = get_user_model()

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = (
            'last_login',
            'is_superuser',
            'is_active',
            'is_staff',
            'groups',
            'user_permissions',
            'history',
            'following'
            )
        extra_kwargs = {
            'password': {'write_only': True},
            'password_conf': {'write_only': True },
            # 'email':{'read_only':True}
        }

    def save(self, **kwargs):
        user = User.objects.create(email=self.validated_data.get('email'),
                    first_name=self.validated_data.get("first_name"),
                    last_name=self.validated_data.get("last_name"),
                    username=self.validated_data.get('username'))

        if self.validated_data.get('password') != self.validated_data.get('password_conf'):
            raise serializers.ValidationError({'message': 'confirm password not match'})
        else:
            user.set_password(self.validated_data.get('password'))
            user.save()
            return user


class relationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relationship
        fields = '__all__'


from rest_framework import serializers
from rest_framework import status
#
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
#
from django.contrib.auth import get_user_model
#
from .models import User, Relationship
#
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # password_conf = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = (
            'last_login',
            'is_superuser',
            'is_active',
            'is_staff',
            'groups',
            'user_permissions',
            'history'
            )
        extra_kwargs = {
            'password': {'write_only': True},
            'password_conf': {'write_only': True },
            # 'email':{'read_only':True}
        }

    def save(self, **kwargs):
        # print(kwargs)
        user = User(email=self.validated_data.get('email'),
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

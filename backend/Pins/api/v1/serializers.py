from Pins.models import Pin
from rest_framework import serializers
from Users.serializers import UserSerializer


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["username"] = UserSerializer(instance.user_id).data["username"]
        representation["profile_image"] = UserSerializer(instance.user_id).data["profile_image"]
        return representation

from Boards.models import Board
from rest_framework import serializers
from Users.serializers import UserSerializer
from Pins.api.v1.serializers import PinSerializer


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = (
            "is_public",
            "is_archived",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["username"] = UserSerializer(instance.created_by).data["username"]
        representation["profile_image"] = UserSerializer(instance.created_by).data["profile_image"]
        representation["cover_image"] = UserSerializer(instance.created_by).data["cover_image"]
        representation["bio"] = UserSerializer(instance.created_by).data["bio"]
        # representation["attachment"] = PinSerializer(instance.pins).data["attachment"]
        # representation["bio"] = UserSerializer(instance.created_by).data["bio"]
        return representation

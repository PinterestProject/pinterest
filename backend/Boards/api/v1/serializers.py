from Boards.models import Board
from rest_framework import serializers
from Users.serializers import UserSerializer

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
        return representation

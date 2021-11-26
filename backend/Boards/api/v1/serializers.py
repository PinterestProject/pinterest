from Boards.models import Board
from rest_framework import serializers


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = (
            "is_public",
            "is_archived",
        )

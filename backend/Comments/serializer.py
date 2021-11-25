from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comments
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = comments_likes
        fields = ['user_id','comment_id']

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = comment_reply
        fields = "__all__"

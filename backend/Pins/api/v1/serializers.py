from Pins.models import Pin
from rest_framework import serializers


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = "__all__"

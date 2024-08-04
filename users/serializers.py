from rest_framework import serializers


class LoginSerializers(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

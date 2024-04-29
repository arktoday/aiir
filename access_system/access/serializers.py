from rest_framework import serializers


class UserSrializer(serializers.Serializer):
    username = serializers.CharField


class UserQuerySerializer(UserSrializer):
    username = serializers.CharField()

from rest_framework import serializers


class NewUsernSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class NewSourceSerializer(serializers.Serializer):
    name = serializers.CharField()
    
    
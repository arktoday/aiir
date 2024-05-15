from rest_framework import serializers


class BasicUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class UserSerializer(BasicUserSerializer):
    username = serializers.CharField()


class AuthUserSerializer(serializers.Serializer):
    auth_user = serializers.SerializerMethodField("get_auth_user")

    def get_auth_user(self, obj):
        return self.context["request"].user


class UserCreateQuerySerializer(AuthUserSerializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SourceCreateQuerySerializer(AuthUserSerializer):
    name = serializers.CharField()


class SourceResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    
    
class BaseRequestAccessSerializer(serializers.Serializer):
    source_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    
    
class SetAccessSerializer(AuthUserSerializer):
    source_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    

class CheckAccessSerializer(serializers.Serializer):
    source_id = serializers.IntegerField()

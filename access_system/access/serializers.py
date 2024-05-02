from rest_framework import serializers

class BasicUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class UserSerializer(BasicUserSerializer):
    username = serializers.CharField()


class UserQuerySerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    auth_user = serializers.SerializerMethodField('get_auth_user')
    
    def get_auth_user(self, obj):
        return self.context['request'].user

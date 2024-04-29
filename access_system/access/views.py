from django.shortcuts import render
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema_view, extend_schema

from access.services.access_service import AccessService
from access import serializers


@extend_schema_view(
    create_user=extend_schema(summary='Create User', 
                              parameters=[serializers.UserQuerySerializer], 
                              responses=serializers.UserSrializer,
                              auth=True
    )
)
class AccessViewSet(ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    access_service = AccessService

    def create_user(self, request):
        query_serializer = serializers.UserQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            raise ValidationError(query_serializer.errors)

        return 1

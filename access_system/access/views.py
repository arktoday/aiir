from typing import Any
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from access.services.access_service import UserService, SourceService, AccessService
from access.serializers import (
    UserCreateQuerySerializer,
    UserSerializer,
    SourceCreateQuerySerializer,
    SourceResponseSerializer,
    AuthUserSerializer,
    SetAccessSerializer,
    BaseRequestAccessSerializer,
    CheckAccessSerializer,
)
from access.models import Source


# @extend_schema_view(
#     create_user=extend_schema(
#         summary="Create User",
#         request=UserQuerySerializer,
#         tags=["User"]
#     ),
# )
class AccessViewSet(ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    access_service = AccessService()

    @extend_schema(
        summary="Set Access To User",
        request=SetAccessSerializer,
        tags=["Access"],
    )
    def set_access(self, request):
        query_serializer = SetAccessSerializer(
            data=request.data, context={"request": request}
        )
        if not query_serializer.is_valid():
            raise ValidationError(query_serializer.errors)

        if query_serializer.data["auth_user"].is_superuser != 1:
            return Response(
                "Only superuser can set access", status=status.HTTP_403_FORBIDDEN
            )

        new_access = self.access_service.set_access(**query_serializer.data)
        return Response(new_access)

    @extend_schema(
        summary="Delete User Access to Source",
        parameters=[BaseRequestAccessSerializer],
        request=AuthUserSerializer,
        tags=["Access"],
    )
    def delete(self, request):
        query_serializer = BaseRequestAccessSerializer(data=request.query_params)
        auth_serializer = AuthUserSerializer(
            data=request.data, context={"request": request}
        )
        if not query_serializer.is_valid():
            raise ValidationError(query_serializer.errors)
        if not auth_serializer.is_valid():
            raise ValidationError(query_serializer.errors)

        if auth_serializer.data["auth_user"].is_superuser != 1:
            return Response(
                "Only superuser can delete access", status=status.HTTP_403_FORBIDDEN
            )

        dropped_access_status = self.access_service.delete_access(
            **query_serializer.data, **auth_serializer.data
        )
        return Response(dropped_access_status)

    @extend_schema(
        summary="Check User Access",
        parameters=[CheckAccessSerializer],
        request=AuthUserSerializer,
        tags=["Access"],
    )
    def get(self, request):
        query_serializer = CheckAccessSerializer(data=request.query_params)
        auth_serializer = AuthUserSerializer(
            data=request.data, context={"request": request}
        )
        if not query_serializer.is_valid():
            raise ValidationError(query_serializer.errors)
        if not auth_serializer.is_valid():
            raise ValidationError(query_serializer.errors)

        access_status = self.access_service.check_access(
            **query_serializer.data, **auth_serializer.data
        )
        return Response(access_status)


class UserViewSet(ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    user_service = UserService()

    @extend_schema(
        summary="Create User",
        request=UserCreateQuerySerializer,
        tags=["User"],
    )
    def create_user(self, request):
        query_serializer = UserCreateQuerySerializer(
            data=request.data, context={"request": request}
        )
        if not query_serializer.is_valid():
            raise ValidationError(query_serializer.errors)

        if query_serializer.data["auth_user"].is_superuser != 1:
            return Response(
                "Only superuser can create new user", status=status.HTTP_403_FORBIDDEN
            )

        user = self.user_service.create_user(**query_serializer.data)

        if user is False:
            return Response(user)

        return Response(UserSerializer(user).data)

    @extend_schema(
        summary="Get Users", request=AuthUserSerializer, tags=["User"], methods=["get"]
    )
    def get(self, request):
        query_serializer = AuthUserSerializer(
            data=request.data, context={"request": request}
        )
        if not query_serializer.is_valid():
            raise ValidationError(query_serializer.errors)
        if query_serializer.data["auth_user"].is_superuser != 1:
            return Response(
                "Only superuser can get all users", status=status.HTTP_403_FORBIDDEN
            )

        users = self.user_service.get_all_users(**query_serializer.data)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class SourceViewSet(ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    source_service = SourceService()

    @extend_schema(
        summary="Create Source",
        request=SourceCreateQuerySerializer,
        tags=["Source"],
    )
    def create_source(self, request):
        query_serializer = SourceCreateQuerySerializer(
            data=request.data, context={"request": request}
        )
        if not query_serializer.is_valid():
            raise ValidationError(query_serializer.errors)

        if query_serializer.data["auth_user"].is_superuser != 1:
            return Response(
                "Only superuser can create new source", status=status.HTTP_403_FORBIDDEN
            )

        source = self.source_service.create_source(**query_serializer.data)
        if source is False:
            return Response(source)

        return Response(SourceResponseSerializer(source).data)

    @extend_schema(
        summary="Get Sources",
        request=AuthUserSerializer,
        tags=["Source"],
        methods=["get"],
    )
    def get(self, request):
        query_serializer = AuthUserSerializer(
            data=request.data, context={"request": request}
        )
        if not query_serializer.is_valid():
            raise ValidationError(query_serializer.errors)
        if query_serializer.data["auth_user"].is_superuser != 1:
            return Response(
                "Only superuser can get all sources", status=status.HTTP_403_FORBIDDEN
            )

        sources = self.source_service.get_all_sources(**query_serializer.data)

        serializer = SourceResponseSerializer(sources, many=True)
        return Response(serializer.data)

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from access.services.access_service import AccessService
from access.serializers import UserQuerySerializer, UserSerializer


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

    # access_service = AccessService()

    @extend_schema(
        summary="Create User",
        request=UserQuerySerializer,
        tags=["User"],
    )
    def create_user(self, request):
        access_service = AccessService()
        query_serializer = UserQuerySerializer(data=request.data, context={'request': request})
        if not query_serializer.is_valid():
            raise ValidationError(query_serializer.errors)

        user = access_service.create_user(**query_serializer.data)
        return Response(user)
        if user is False:
            return Response(user)

        return Response(UserSerializer(user).data)

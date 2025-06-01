from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.constants import (ALREADY_SUBSCRIBED_ERROR,
                            INCORRECT_CURRENT_PASSWORD_ERROR,
                            NOT_SUBSCRIBED_ERROR, PAGE_NOT_FOUND_ERROR,
                            REQUIRED_FIELD_ERROR, SUBSCRIBE_TO_YOURSELF_ERROR)
from core.pagination import LimitPageNumberPagination
from core.permissions import IsAuthenticatedOrReadOnlyUser, IsSelfOrAdmin

from ..models import Subscription, User
from ..serializers import (UserCreateSerializer, UserSerializer,
                           UserWithRecipesSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsAuthenticatedOrReadOnlyUser]
        elif self.action in ['me', 'avatar', 'set_password', 'subscribe', 'unsubscribe', 'subscriptions']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsSelfOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(
            serializer.data
        )

    @action(detail=False, methods=['put', 'delete'], url_path='me/avatar')
    def avatar(self, request):
        user = request.user

        if request.method == 'PUT':
            avatar_data = request.data.get('avatar')
            if not avatar_data:
                return Response(
                    {'avatar': [REQUIRED_FIELD_ERROR]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.get_serializer(
                user,
                data={'avatar': avatar_data},
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                avatar_url = serializer.data.get('avatar')
                return Response(
                    {'avatar': avatar_url},
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user.avatar.delete(save=True)
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['post'], url_path='set_password')
    def set_password(self, request):
        user = request.user
        current_pass = request.data.get('current_password')
        new_pass = request.data.get('new_password')

        errors = {}
        if not current_pass:
            errors['current_password'] = [REQUIRED_FIELD_ERROR]
        if not new_pass:
            errors['new_password'] = [REQUIRED_FIELD_ERROR]
        if errors:
            return Response(
                errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(current_pass):
            return Response(
                {'current_password': [INCORRECT_CURRENT_PASSWORD_ERROR]},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_pass)
        user.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        user = request.user
        try:
            author = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'detail': PAGE_NOT_FOUND_ERROR},
                status=status.HTTP_404_NOT_FOUND
            )

        if user == author:
            return Response(
                {'detail': SUBSCRIBE_TO_YOURSELF_ERROR},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.subscriptions.filter(author=author).exists():
            return Response(
                {'detail': ALREADY_SUBSCRIBED_ERROR},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.subscriptions.create(author=author)
        serializer = UserWithRecipesSerializer(
            author,
            context={'request': request}
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @subscribe.mapping.delete
    def unsubscribe(self, request, pk=None):
        user = request.user
        try:
            author = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'detail': PAGE_NOT_FOUND_ERROR},
                status=status.HTTP_404_NOT_FOUND
            )

        subscription = user.subscriptions.filter(author=author)
        if not subscription.exists():
            return Response(
                {'detail': NOT_SUBSCRIBED_ERROR},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        subscriptions = request.user.subscriptions.select_related('author')
        authors = [sub.author for sub in subscriptions]

        paginator = LimitPageNumberPagination()
        result_page = paginator.paginate_queryset(authors, request)

        serializer = UserWithRecipesSerializer(
            result_page,
            many=True,
            context={'request': request}
        )
        return paginator.get_paginated_response(serializer.data)

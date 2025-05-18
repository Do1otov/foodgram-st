from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.pagination import LimitPageNumberPagination
from core.permissions import UserPermission

from ..models import Subscription, User
from ..serializers import (UserCreateSerializer, UserSerializer,
                           UserWithRecipesSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [UserPermission]
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'delete'], url_path='me/avatar')
    def avatar(self, request):
        user = request.user

        if request.method == 'PUT':
            avatar_data = request.data.get('avatar')
            if not avatar_data:
                return Response({'avatar': ['Обязательное поле.']}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(user, data={'avatar': avatar_data}, partial=True)
            if serializer.is_valid():
                serializer.save()
                avatar_url = serializer.data.get('avatar')
                return Response({'avatar': avatar_url}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user.avatar.delete(save=True)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='set_password')
    def set_password(self, request):
        user = request.user
        current_pass = request.data.get('current_password')
        new_pass = request.data.get('new_password')

        errors = {}
        if not current_pass:
            errors['current_password'] = ['Обязательное поле.']
        if not new_pass:
            errors['new_password'] = ['Обязательное поле.']
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_pass):
            return Response({'current_password': ['Неверный текущий пароль.']}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_pass)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        user = request.user
        try:
            author = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'Страница не найдена.'}, status=404)

        if user == author:
            return Response({'detail': 'Нельзя подписаться на самого себя.'}, status=400)
        if Subscription.objects.filter(user=user, author=author).exists():
            return Response({'detail': 'Вы уже подписаны.'}, status=400)

        Subscription.objects.create(user=user, author=author)
        serializer = UserWithRecipesSerializer(author, context={'request': request})
        return Response(serializer.data, status=201)

    @subscribe.mapping.delete
    def unsubscribe(self, request, pk=None):
        user = request.user
        try:
            author = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'Страница не найдена.'}, status=404)

        subscription = Subscription.objects.filter(user=user, author=author)
        if not subscription.exists():
            return Response({'detail': 'Вы не были подписаны.'}, status=400)

        subscription.delete()
        return Response(status=204)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribers__user=user)

        paginator = LimitPageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = UserWithRecipesSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

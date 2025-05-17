from rest_framework.permissions import BasePermission


class UserViewSetPermission(BasePermission):
    """
    Единый permission-класс для UserViewSet.
    """

    def has_permission(self, request, view):
        user = request.user
        action = view.action

        # Неавторизованный пользователь
        if not user.is_authenticated:
            return action in ['list', 'retrieve', 'create']

        # Администратор
        if user.is_staff:
            return True

        # Авторизованный пользователь
        if action in [
            'me', 'set_password', 'avatar', 'delete_avatar',
            'subscribe', 'unsubscribe', 'subscriptions',
            'list', 'retrieve'
        ]:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        action = view.action

        # Администратор
        if user.is_staff:
            return True

        # Пользователь может получать/менять только свой профиль
        if action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return obj == user

        return False

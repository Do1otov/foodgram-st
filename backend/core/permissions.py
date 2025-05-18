from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        action = view.action

        if not user.is_authenticated:
            return action in ['list', 'retrieve', 'create']

        if user.is_staff:
            return True

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

        if user.is_staff:
            return True

        if action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return obj == user

        return False


class RecipePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user or request.user.is_staff

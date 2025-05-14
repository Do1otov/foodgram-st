from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from core.utils import decode_base64_image


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]


    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer


    def get_permissions(self):
        if self.action in ['me', 'set_password', 'avatar', 'delete_avatar']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()


    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


    @action(detail=False, methods=['put', 'delete'], url_path='me/avatar')
    def avatar(self, request):
        if request.method == 'PUT':
            avatar_data = request.data.get('avatar')
            if not avatar_data:
                return Response({'avatar': ['Обязательное поле.']}, status=status.HTTP_400_BAD_REQUEST)

            try:
                avatar_file = decode_base64_image(avatar_data, 'avatar')
                request.user.avatar = avatar_file
                request.user.save()
                return Response({'avatar': request.user.avatar.url})
            except ValueError as e:
                return Response({'avatar': [str(e)]}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            request.user.avatar.delete(save=True)
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

from rest_framework import serializers
from .models import User
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_subscribed', 'avatar')

    def get_is_subscribed(self, obj):
        return False  # заглушка

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

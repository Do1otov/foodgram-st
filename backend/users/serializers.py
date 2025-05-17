from rest_framework import serializers
from .models import User
from .models import Subscription
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_subscribed', 'avatar')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and Subscription.objects.filter(user=user, author=obj).exists()
        )

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserWithRecipesSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, obj):
        from recipes.serializers import ShortRecipeSerializer

        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        recipes = obj.recipes.all()  # related_name в модели Recipe: author -> recipes
        if limit:
            recipes = recipes[:int(limit)]
        return ShortRecipeSerializer(recipes, many=True, context={'request': request}).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
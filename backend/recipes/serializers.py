from rest_framework import serializers
from .models import Ingredient, Recipe, IngredientInRecipe, Favorite, ShoppingCart
from users.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from django.core.exceptions import ValidationError as DjangoValidationError


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientInRecipeWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), source='ingredient')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class IngredientInRecipeReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.ListField(
        child=serializers.DictField(), write_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['ingredients'] = IngredientInRecipeReadSerializer(
            instance.ingredientinrecipe_set.all(), many=True
        ).data
        return rep

    def validate_ingredients(self, value):
        if not isinstance(value, list) or not value:
            raise serializers.ValidationError('Нужен хотя бы один ингредиент.')

        if len(value) > 100:
            raise serializers.ValidationError('Максимум 100 ингредиентов.')

        seen_ids = set()
        for item in value:
            if not isinstance(item, dict):
                raise serializers.ValidationError('Ингредиенты должны быть словарями.')
            ingredient_id = item.get('id')
            amount = item.get('amount')
            if ingredient_id in seen_ids:
                raise serializers.ValidationError('Ингредиенты не должны повторяться.')
            seen_ids.add(ingredient_id)
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError(f'Ингредиент с id={ingredient_id} не найден.')
            if not (1 <= int(amount) <= 32767):
                raise serializers.ValidationError('Количество должно быть от 1 до 32767.')
        return value

    def add_ingredients(self, recipe, ingredients_data):
        for item in ingredients_data:
            ingredient = Ingredient.objects.get(pk=item['id'])
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=item['amount']
            )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        try:
            recipe = Recipe.objects.create(**validated_data)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict if hasattr(e, 'message_dict') else str(e))

        self.add_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if ingredients_data is not None:
            instance.ingredientinrecipe_set.all().delete()
            self.add_ingredients(instance, ingredients_data)

        return instance

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()





class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

from django.core.exceptions import ValidationError as DjangoValidationError
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from core.constants import (INGREDIENT_IN_RECIPE_NOT_FOUND,
                            INGREDIENTS_IN_RECIPE_MAX_NUM,
                            INGREDIENTS_IN_RECIPE_NOT_MAP_ERROR,
                            MAX_NUM_INGREDIENTS_IN_RECIPE_ERROR,
                            MIN_MAX_INGREDIENTS_IN_RECIPE_ERROR,
                            POS_INT_FIELD_MAX, POS_INT_FIELD_MIN,
                            REPEATING_INGREDIENTS_IN_RECIPE_ERROR,
                            REQUIRED_FIELD_ERROR,
                            ZERO_INGREDIENTS_IN_RECIPE_ERROR)
from users.serializers import UserSerializer

from ..models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                      ShoppingCart)
from .ingredient import IngredientInRecipeSerializer


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None,
        use_url=True,
        required=True,
        allow_null=False,
        allow_empty_file=False
    )
    author = UserSerializer(
        read_only=True
    )
    ingredients = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
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
        rep['ingredients'] = IngredientInRecipeSerializer(
            instance.ingredientinrecipe_set.all(), many=True
        ).data
        return rep

    def validate_ingredients(self, value):
        if not isinstance(value, list) or not value:
            raise serializers.ValidationError(ZERO_INGREDIENTS_IN_RECIPE_ERROR)

        if len(value) > INGREDIENTS_IN_RECIPE_MAX_NUM:
            raise serializers.ValidationError(MAX_NUM_INGREDIENTS_IN_RECIPE_ERROR)

        seen_ids = set()
        for item in value:
            if not isinstance(item, dict):
                raise serializers.ValidationError(INGREDIENTS_IN_RECIPE_NOT_MAP_ERROR)
            ingredient_id = item.get('id')
            amount = item.get('amount')
            if ingredient_id in seen_ids:
                raise serializers.ValidationError(REPEATING_INGREDIENTS_IN_RECIPE_ERROR)
            seen_ids.add(ingredient_id)
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError(INGREDIENT_IN_RECIPE_NOT_FOUND.format(id=ingredient_id))
            if not (POS_INT_FIELD_MIN <= int(amount) <= POS_INT_FIELD_MAX):
                raise serializers.ValidationError(MIN_MAX_INGREDIENTS_IN_RECIPE_ERROR)
        return value

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError({ 'image': REQUIRED_FIELD_ERROR })
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
        if 'ingredients' not in validated_data:
            raise serializers.ValidationError({
                'ingredients': REQUIRED_FIELD_ERROR
            })

        ingredients_data = validated_data.pop('ingredients')

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

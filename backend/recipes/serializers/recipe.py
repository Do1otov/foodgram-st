from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from core.constants import (
    INGREDIENTS_IN_RECIPE_MAX_NUM,
    MAX_NUM_INGREDIENTS_IN_RECIPE_ERROR,
    REPEATING_INGREDIENTS_IN_RECIPE_ERROR,
    REQUIRED_FIELD_ERROR,
    ZERO_INGREDIENTS_IN_RECIPE_ERROR,
)
from users.serializers import UserSerializer
from ..models import IngredientInRecipe, Recipe
from .ingredient import (
    IngredientInRecipeReadSerializer,
    IngredientInRecipeWriteSerializer,
)


class RecipeReadSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(
        read_only=True
    )
    ingredients = IngredientInRecipeReadSerializer(
        source='ingredient_links',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return (
            not user.is_anonymous
            and obj.favorite.filter(user=user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (
            not user.is_anonymous
            and obj.shopping_cart.filter(user=user).exists()
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None,
        use_url=True,
        required=True,
        allow_null=False,
        allow_empty_file=False
    )
    ingredients = IngredientInRecipeWriteSerializer(
        many=True,
        write_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'ingredients', 'name', 'image',
            'text', 'cooking_time'
        )

    def validate(self, data):
        if (
            'image' not in self.initial_data
            or not self.initial_data.get('image')
        ):
            raise serializers.ValidationError({
                'image': REQUIRED_FIELD_ERROR
            })

        ingredients = self.initial_data.get('ingredients')
        if ingredients is None:
            raise serializers.ValidationError({
                'ingredients': REQUIRED_FIELD_ERROR
            })
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': ZERO_INGREDIENTS_IN_RECIPE_ERROR
            })
        if len(ingredients) > INGREDIENTS_IN_RECIPE_MAX_NUM:
            raise serializers.ValidationError({
                'ingredients': MAX_NUM_INGREDIENTS_IN_RECIPE_ERROR
            })

        ingredient_ids = set()
        for item in ingredients:
            ingredient_id = item.get('id')
            if ingredient_id in ingredient_ids:
                raise serializers.ValidationError({
                    'ingredients': REPEATING_INGREDIENTS_IN_RECIPE_ERROR
                })
            ingredient_ids.add(ingredient_id)

        return data

    def add_ingredients(self, recipe, ingredients_data):
        IngredientInRecipe.objects.bulk_create([
            IngredientInRecipe(
                recipe=recipe,
                ingredient=item['id'],
                amount=item['amount']
            )
            for item in ingredients_data
        ])

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = super().create(validated_data)
        self.add_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')

        super().update(instance, validated_data)

        if ingredients_data is not None:
            instance.ingredient_links.all().delete()
            self.add_ingredients(instance, ingredients_data)

        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context=self.context
        ).data

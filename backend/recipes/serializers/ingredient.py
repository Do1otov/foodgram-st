from rest_framework import serializers

from core.constants import (
    MIN_MAX_INGREDIENTS_IN_RECIPE_ERROR,
    POS_INT_FIELD_MAX,
    POS_INT_FIELD_MIN,
)
from ..models import Ingredient, IngredientInRecipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientInRecipeReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientInRecipeWriteSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(
        min_value=POS_INT_FIELD_MIN,
        max_value=POS_INT_FIELD_MAX,
        error_messages={
            'min_value': MIN_MAX_INGREDIENTS_IN_RECIPE_ERROR,
            'max_value': MIN_MAX_INGREDIENTS_IN_RECIPE_ERROR
        }
    )

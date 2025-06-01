from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from ..models import Recipe


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

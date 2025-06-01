from rest_framework import serializers

from .user import UserSerializer



class UserWithRecipesSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(source='recipes.count', read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, obj):
        from recipes.serializers import ShortRecipeSerializer
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = None

        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:limit]

        return ShortRecipeSerializer(
            recipes,
            many=True,
            context={'request': request}
        ).data

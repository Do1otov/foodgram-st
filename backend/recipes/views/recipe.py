from django.http import Http404, HttpResponse
from django.utils.timezone import localdate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.constants import MONTHS_IN_RUSSIAN_MAP
from core.pagination import LimitPageNumberPagination
from core.permissions import RecipePermission

from ..filters import RecipeFilter
from ..models import Favorite, IngredientInRecipe, Recipe, ShoppingCart
from ..serializers import RecipeSerializer, ShortRecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [RecipePermission]
    pagination_class = LimitPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_object_or_404_recipe(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404('Рецепт не найден.')
        
    def add_to(self, model, request, pk):
        user = request.user
        recipe = self.get_object_or_404_recipe(pk)
        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'errors': 'Рецепт уже добавлен.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        model.objects.create(user=user, recipe=recipe)
        return Response(ShortRecipeSerializer(recipe, context=self.get_serializer_context()).data, status=status.HTTP_201_CREATED)

    def remove_from(self, model, request, pk):
        user = request.user
        recipe = self.get_object_or_404_recipe(pk)
        obj = model.objects.filter(user=user, recipe=recipe).first()
        if not obj:
            return Response(
                {'errors': 'Рецепт не найден в списке.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        return self.add_to(Favorite, request, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return self.remove_from(Favorite, request, pk)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self.add_to(ShoppingCart, request, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.remove_from(ShoppingCart, request, pk)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_short_link(self, request, pk=None):
        try:
            recipe = self.get_object()
        except Recipe.DoesNotExist:
            return Response(
                {'detail': 'Рецепт не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        short_link = request.build_absolute_uri(f'/s/{recipe.short_link_code}')
        return Response({'short-link': short_link}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        recipes = Recipe.objects.filter(shopping_cart__user=user)

        if not recipes.exists():
            return Response({'detail': 'Список покупок пуст.'}, status=400)

        recipe_names = sorted(recipes.values_list('name', flat=True))
        date = localdate()
        date_str = f'{date.day} {MONTHS_IN_RUSSIAN_MAP[date.month]} {date.year} г.'
        recipe_line = f'{"Рецепт" if len(recipe_names) == 1 else "Рецепты"}: {", ".join(recipe_names)}.'

        ingredients = {}
        for item in IngredientInRecipe.objects.filter(recipe__in=recipes):
            name = item.ingredient.name.capitalize()
            key = (name, item.ingredient.measurement_unit)
            ingredients[key] = ingredients.get(key, 0) + item.amount

        sorted_items = sorted(ingredients.items(), key=lambda x: x[0][0])

        lines = [f'Список покупок от {date_str}', recipe_line, 'Продукты:']
        for i, ((name, unit), amount) in enumerate(sorted_items, 1):
            lines.append(f'{i}. {name} — {amount} {unit}.')

        response = HttpResponse('\n'.join(lines), content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="shopping-list.txt"'
        return response

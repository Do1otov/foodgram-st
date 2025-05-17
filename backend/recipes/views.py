from rest_framework import viewsets, permissions, status
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ingredient, Recipe, Favorite, ShoppingCart
from .serializers import IngredientSerializer, RecipeSerializer, ShortRecipeSerializer
from django.http import Http404
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .filters import IngredientFilter
from rest_framework.pagination import PageNumberPagination
from .filters import RecipeFilter


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    pagination_class = None


class RecipePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = RecipePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_object_or_404_recipe(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404("Рецепт не найден.")
        
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
                {"detail": "Рецепт не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        short_link = request.build_absolute_uri(f'/s/{recipe.short_link_code}')
        return Response({"short-link": short_link}, status=status.HTTP_200_OK)


class ShortLinkRedirectView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, short_link_code):
        try:
            recipe = Recipe.objects.get(short_link_code=short_link_code)
        except Recipe.DoesNotExist:
            raise Http404("Рецепт не найден.")

        return redirect(f'http://localhost/recipes/{recipe.id}')

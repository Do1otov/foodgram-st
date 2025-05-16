from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipes.views import IngredientViewSet, RecipeViewSet


router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]

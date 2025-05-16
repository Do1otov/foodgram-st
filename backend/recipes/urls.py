from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipes.views import IngredientViewSet


router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]

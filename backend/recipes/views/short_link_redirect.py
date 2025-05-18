from django.http import Http404
from django.shortcuts import redirect
from rest_framework.views import APIView

from ..models import Recipe
from core.constants import RECIPE_SHORT_LINK_REDIRECT_URL


class ShortLinkRedirectView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, short_link_code):
        try:
            recipe = Recipe.objects.get(short_link_code=short_link_code)
        except Recipe.DoesNotExist:
            raise Http404('Рецепт не найден.')

        return redirect(RECIPE_SHORT_LINK_REDIRECT_URL.format(id=recipe.id))

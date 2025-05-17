from rest_framework.views import APIView
from django.http import Http404
from django.shortcuts import redirect
from ..models import Recipe


class ShortLinkRedirectView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, short_link_code):
        try:
            recipe = Recipe.objects.get(short_link_code=short_link_code)
        except Recipe.DoesNotExist:
            raise Http404('Рецепт не найден.')

        return redirect(f'http://localhost/recipes/{recipe.id}')

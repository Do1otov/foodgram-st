from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from core.constants import (RECIPE_NOT_FOUND_ERROR,
                            RECIPE_URL)

from ..models import Recipe


class ShortLinkRedirectView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, short_link_code):
        try:
            recipe = Recipe.objects.get(short_link_code=short_link_code)
        except Recipe.DoesNotExist:
            raise NotFound(RECIPE_NOT_FOUND_ERROR)

        redirect_path = RECIPE_URL.format(id=recipe.id)
        redirect_url = request.build_absolute_uri(redirect_path)

        return Response(
            data={'detail': 'Redirecting'},
            status=status.HTTP_302_FOUND,
            headers={'Location': redirect_url}
        )

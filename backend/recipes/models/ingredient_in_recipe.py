from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.constants import POS_INT_FIELD_MAX, POS_INT_FIELD_MIN

from .ingredient import Ingredient
from .recipe import Recipe


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_links',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(POS_INT_FIELD_MIN),
            MaxValueValidator(POS_INT_FIELD_MAX)
        ],
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'ингредиента в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'recipe',
                    'ingredient'
                ],
                name='unique_ingredient_per_recipe'
            )
        ]

    def __str__(self):
        return (
            f'{self.ingredient.name}, {self.amount} '
            f'{self.ingredient.measurement_unit}'
        )

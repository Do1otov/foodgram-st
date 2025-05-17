from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .recipe import Recipe
from .ingredient import Ingredient


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(32767)],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'ингредиента в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_per_recipe')
        ]

    def __str__(self):
        return f'{self.ingredient.name}, {self.amount} {self.ingredient.measurement_unit}'

from django.db import models
from django.contrib.auth import get_user_model
from core.models import CreatedModel
from django.core.validators import MinLengthValidator
from django.core.validators import MinValueValidator, MaxValueValidator


class Ingredient(models.Model):
    name = models.CharField(
        max_length=128,
        validators=[
            MinLengthValidator(1)
        ],
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=64,
        validators=[
            MinLengthValidator(1)
        ],
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'ингредиента'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


User = get_user_model()


class Recipe(CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=256,
        validators=[
            MinLengthValidator(1)
        ],
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение'
    )
    text = models.TextField(
        validators=[
            MinLengthValidator(1)
        ],
        verbose_name='Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(32767)],
        verbose_name='Время приготовления (мин)'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты'
    )

    class Meta:
        verbose_name = 'рецепта'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


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
        return f"{self.ingredient.name}, {self.amount} {self.ingredient.measurement_unit}"

from django.db import models
from django.contrib.auth import get_user_model
from core.models import CreatedModel
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from core.utils import generate_short_link_code
from core.constants import SHORT_LINK_CODE_MAX_LEN, SHORT_LINK_CODE_MAX_ATTEMPTS_GENERATE


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
    short_link_code = models.CharField(
        max_length=SHORT_LINK_CODE_MAX_LEN,
        unique=True,
        editable=False,
        verbose_name='Код короткой ссылки'
    )

    class Meta:
        verbose_name = 'рецепта'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.short_link_code:
            for _ in range(SHORT_LINK_CODE_MAX_ATTEMPTS_GENERATE):
                code = generate_short_link_code()
                if not Recipe.objects.filter(short_link_code=code).exists():
                    self.short_link_code = code
                    break
            else:
                raise ValidationError("Произошла ошибка при генерации короткой ссылки. Пожалуйста, попробуйте позже.")
        super().save(*args, **kwargs)

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


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='favorite')

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_cart')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='shopping_cart')

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
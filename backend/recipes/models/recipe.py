from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models

from core.constants import (SHORT_LINK_CODE_MAX_ATTEMPTS_GENERATE,
                            RECIPE_SHORT_LINK_CODE_MAX_LEN)
from core.utils import generate_short_link_code

from .ingredient import Ingredient
from core.constants import RECIPE_NAME_MAX_LEN, CHAR_FIELD_MIN_LEN, POS_INT_FIELD_MIN, POS_INT_FIELD_MAX

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=RECIPE_NAME_MAX_LEN,
        validators=[
            MinLengthValidator(CHAR_FIELD_MIN_LEN)
        ],
        verbose_name='Название',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение',
    )
    text = models.TextField(
        validators=[
            MinLengthValidator(CHAR_FIELD_MIN_LEN)
        ],
        verbose_name='Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(POS_INT_FIELD_MIN),
            MaxValueValidator(POS_INT_FIELD_MAX)
        ],
        verbose_name='Время приготовления (мин)',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты',
    )
    short_link_code = models.CharField(
        max_length=RECIPE_SHORT_LINK_CODE_MAX_LEN,
        unique=True,
        editable=False,
        verbose_name='Код короткой ссылки',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
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
                raise ValidationError('Произошла ошибка при генерации короткой ссылки. Пожалуйста, попробуйте позже.')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

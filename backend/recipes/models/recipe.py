from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from core.utils import generate_short_link_code
from core.constants import SHORT_LINK_CODE_MAX_LEN, SHORT_LINK_CODE_MAX_ATTEMPTS_GENERATE
from .ingredient import Ingredient


User = get_user_model()


class Recipe(models.Model):
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
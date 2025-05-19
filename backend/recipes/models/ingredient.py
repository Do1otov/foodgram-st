from django.core.validators import MinLengthValidator
from django.db import models

from core.constants import (CHAR_FIELD_MIN_LEN,
                            INGREDIENT_MEASUREMENT_UNIT_MAX_LEN,
                            INGREDIENT_NAME_MAX_LEN)


class Ingredient(models.Model):
    name = models.CharField(
        max_length=INGREDIENT_NAME_MAX_LEN,
        validators=[
            MinLengthValidator(CHAR_FIELD_MIN_LEN)
        ],
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=INGREDIENT_MEASUREMENT_UNIT_MAX_LEN,
        validators=[
            MinLengthValidator(CHAR_FIELD_MIN_LEN)
        ],
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'ингредиента'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'name',
                    'measurement_unit'
                ],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

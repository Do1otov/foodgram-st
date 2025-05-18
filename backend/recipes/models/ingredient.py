from django.core.validators import MinLengthValidator
from django.db import models


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
                fields=[
                    'name',
                    'measurement_unit'
                ],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

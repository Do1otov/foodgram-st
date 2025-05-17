from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=254
    )
    username = models.CharField(
        verbose_name='Никнейм',
        unique=True,
        max_length=150,
        validators=[MinLengthValidator(1, _('Имя пользователя не может быть пустым.'))]
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        validators=[MinLengthValidator(1, _('Имя не может быть пустым.'))]
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        validators=[MinLengthValidator(1, _('Фамилия не может быть пустой.'))]
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='users/',
        blank=True,
        null=True
    )
    is_staff = models.BooleanField(
        verbose_name='Является админом',
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name='Активная учётная запись',
        default=True,
    )
    date_joined = models.DateTimeField(
        verbose_name='Дата регистрации',
        default=timezone.now
    )
    last_login = models.DateTimeField(
        verbose_name='Последний вход',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор рецептов'
    )

    class Meta:
        unique_together = ('user', 'author')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
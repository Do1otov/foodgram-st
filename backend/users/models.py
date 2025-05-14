from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


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
        max_length=150
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150
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
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.constants import USER_EMAIL_MAX_LEN, USER_USERNAME_MAX_LEN, USER_FIRST_NAME_MAX_LEN, USER_LAST_NAME_MAX_LEN, CHAR_FIELD_MIN_LEN


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = models.EmailField(
        max_length=USER_EMAIL_MAX_LEN,
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    username = models.CharField(
        max_length=USER_USERNAME_MAX_LEN,
        unique=True,
        validators=[MinLengthValidator(CHAR_FIELD_MIN_LEN, _('Никнейм не может быть пустым.'))],
        verbose_name='Никнейм',
    )
    first_name = models.CharField(
        max_length=USER_FIRST_NAME_MAX_LEN,
        validators=[MinLengthValidator(CHAR_FIELD_MIN_LEN, _('Имя не может быть пустым.'))],
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=USER_LAST_NAME_MAX_LEN,
        validators=[MinLengthValidator(CHAR_FIELD_MIN_LEN, _('Фамилия не может быть пустой.'))],
        verbose_name='Фамилия',
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to='users/',
        verbose_name='Аватар',
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Является админом',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активная учётная запись',
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата регистрации',
    )
    last_login = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Последний вход',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

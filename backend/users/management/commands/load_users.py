import json

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()


class Command(BaseCommand):
    help = 'Загружает пользователей из JSON-файла'

    def add_arguments(self, parser):
        parser.add_argument(
            'filepath',
            type=str,
            help='Путь к JSON-файлу с пользователями'
        )

    def handle(self, *args, **kwargs):
        filepath = kwargs['filepath']

        with open(filepath, encoding='utf-8') as file:
            users_data = json.load(file)

        created_count = 0
        for user_data in users_data:
            if User.objects.filter(username=user_data['username']).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f'Пользователь {user_data["username"]} уже существует'
                    )
                )
                continue

            user = User.objects.create_user(**user_data)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(
                f'Создан пользователь: {user.username} ({user.email})'
            ))

        self.stdout.write(self.style.SUCCESS(
            f'Всего создано пользователей: {created_count}'
        ))

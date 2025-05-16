import json
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает ингредиенты из JSON-файла в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Путь к JSON-файлу с ингредиентами')

    def handle(self, *args, **kwargs):
        filepath = kwargs['filepath']

        with open(filepath, encoding='utf-8') as file:
            data = json.load(file)

        created_count = 0
        for item in data:
            obj, created = Ingredient.objects.get_or_create(
                name=item['name'],
                measurement_unit=item['measurement_unit']
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Загружено {created_count} новых ингредиентов.'))

import base64
import json
import re

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from recipes.models import Recipe, Ingredient, IngredientInRecipe

User = get_user_model()

image_format_re = re.compile(r'data:image/(?P<ext>[^;]+);base64,(?P<data>.+)')


class Command(BaseCommand):
    help = 'Загружает рецепты из JSON-файла в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            'filepath',
            type=str,
            help='Путь к JSON-файлу с рецептами'
        )

    def handle(self, *args, **kwargs):
        filepath = kwargs['filepath']

        with open(filepath, encoding='utf-8') as file:
            recipes_data = json.load(file)

        created_count = 0
        for item in recipes_data:
            username = item.pop('author')
            try:
                author = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f'Автор с username="{username}" не найден. '
                    f'Пропуск рецепта.'
                ))
                continue

            image_data = item.pop('image')
            match = image_format_re.match(image_data)
            if not match:
                self.stdout.write(self.style.ERROR(
                    f'Неверный формат изображения. Пропуск рецепта.'
                ))
                continue

            ext = match.group('ext')
            img_data = match.group('data')
            img_name = f"{item['name'].replace(' ', '_')}.{ext}"
            image = ContentFile(base64.b64decode(img_data), name=img_name)

            ingredients_data = item.pop('ingredients', [])

            if Recipe.objects.filter(
                author=author,
                name=item['name'],
                text=item['text'],
                cooking_time=item['cooking_time']
            ).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f'Рецепт "{item["name"]}" уже существует. Пропуск'
                    )
                )
                continue

            recipe = Recipe.objects.create(
                author=author,
                image=image,
                **item
            )

            for ingredient_data in ingredients_data:
                ingredient_id = ingredient_data.get('id')
                amount = ingredient_data.get('amount')

                try:
                    ingredient = Ingredient.objects.get(id=ingredient_id)
                except Ingredient.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f'Ингредиент с id={ingredient_id} не найден. Пропуск'
                    ))
                    continue

                IngredientInRecipe.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount
                )

            self.stdout.write(self.style.SUCCESS(
                f'Создан рецепт: {recipe.name} для {author.username}'
            ))
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Всего создано рецептов: {created_count}'
        ))

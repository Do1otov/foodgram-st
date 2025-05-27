#!/bin/sh

until nc -z $DB_HOST $DB_PORT; do
  echo "Ожидание базы данных на $DB_HOST:$DB_PORT..."
  sleep 1
done

echo "Миграции..."
python manage.py migrate --noinput

echo "Статика..."
python manage.py collectstatic --noinput

if [ "$INIT_DB" = "true" ]; then
  echo "Загрузка ингредиентов..."
  python manage.py load_ingredients data/ingredients.json

  echo "Загрузка пользователей..."
  python manage.py load_users data/users.json

  echo "Загрузка рецептов..."
  python manage.py load_recipes data/recipes.json

  if [ "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Создание суперпользователя..."
    python manage.py createsuperuser \
      --noinput \
      --email "$DJANGO_SUPERUSER_EMAIL" \
      --username "$DJANGO_SUPERUSER_USERNAME" \
      --first_name "$DJANGO_SUPERUSER_USERNAME" \
      --last_name "$DJANGO_SUPERUSER_USERNAME"
  fi
else
  echo "INIT_DB не указан или не равен 'true' — пропуск загрузки данных"
fi

echo "Запуск Gunicorn..."
gunicorn foodgram_api.wsgi:application --bind 0.0.0.0:8000

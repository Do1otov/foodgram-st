#!/bin/sh
echo "Миграции..."
python manage.py migrate --noinput

echo "Статика..."
python manage.py collectstatic --noinput

echo "Загрузка ингредиентов..."
python manage.py load_ingredients data/ingredients.json

if [ "$DJANGO_SUPERUSER_EMAIL" ]; then
  echo "Суперпользователь..."
  python manage.py createsuperuser \
    --noinput \
    --email "$DJANGO_SUPERUSER_EMAIL" \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --first_name "$DJANGO_SUPERUSER_FIRSTNAME" \
    --last_name "$DJANGO_SUPERUSER_LASTNAME"
fi

echo "Gunicorn..."
gunicorn foodgram_api.wsgi:application --bind 0.0.0.0:8000

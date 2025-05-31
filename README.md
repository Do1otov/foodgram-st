# Foodgram  (итоговый проект от Яндекс Практикума)

[![Foodgram CI/CD](https://github.com/Do1otov/foodgram-st/actions/workflows/main.yml/badge.svg)](https://github.com/Do1otov/foodgram-st/actions/workflows/main.yml)

## Описание проекта

**Foodgram** — сайт для обмена кулинарными идеями, где пользователи могут публиковать свои рецепты, добавлять чужие в избранное и подписываться на любимых авторов. Зарегистрированным пользователям доступна функция «Список покупок» — она формирует список ингредиентов для выбранных блюд, чтобы упростить поход в магазин.

## Стек технологий

- **Python 3.10**, **Django**, **Django REST Framework**
- **PostgreSQL**
- **Gunicorn**
- **Nginx**
- **Docker, Docker Compose**
- **GitHub Actions** (CI/CD)
- **JWT аутентификация (djoser)**

## Развёртывание проекта

### Локальный запуск

**1. Убедитесь, что Docker установлен и запущен:**

```bash
sudo systemctl status docker
```

Если Docker не установлен, то установите его для своей ОС, следуя официальной документации по установке: [Ссылка на документацию по установке](https://docs.docker.com/engine/install/)

Если Docker установлен, но не запущен, выполните:

```bash
sudo systemctl start docker
```

---

**2. Склонируйте репозиторий:**

```bash
git clone https://github.com/Do1otov/foodgram-st.git
cd foodgram-st/
```

---

**3. Создайте `.env` файл в директории `infra/` и заполните его по образу из файла `infra/.env.example`:**

```
# Django
DEBUG=false
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# DB
USE_PGSQL=true
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

POSTGRES_DB=foodgram
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Суперпользователь
DJANGO_SUPERUSER_EMAIL=admin@admin.com
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin

# Загрузка данных
INIT_DB=true
```

Флаг `INIT_DB` отвечает за предзаполнение базы данных. Оставьте `true`, если хотите предзаполнить БД.

---

**4. Запустите проект:**

```bash
docker compose -f docker-compose.prod.yml up -d
```

Чтобы остановить проект, выполните:

```bash
docker compose -f docker-compose.prod.yml down
```

---

**5. Доступность сайта:**
- Главная страница: http://localhost/
- Админка: http://localhost/admin/
- Документация API: http://localhost/api/docs/


## Серверная версия

Проект развёрнут и доступен:
- Главная страница: http://109.120.151.181/
- Админка: http://109.120.151.181/admin/
- Документация API: http://109.120.151.181/api/docs/

## Предзаполнение базы данных

Если в `.env` файле флаг `INIT_DB=true`, то при первом локальном запуске проекта происходит инициализация базы данных игредиентами, суперпользователем и тремя пользователями, каждый из которых имеет по 3 рецепта.

### Данные для входа:

| Email | Пароль | Имя, фамилия | Роль |
| :- | :- | :- | :- |
| user1@test.ru | user1 | Алексей Петров | Пользователь |
| user2@test.ru | user2 | Елена Смирнова | Пользователь |
| user3@test.ru | user3 | Иван Козлов | Пользователь |
| admin@admin.com | admin | admin admin | Админ |


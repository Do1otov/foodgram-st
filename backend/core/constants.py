# Общая валидация моделей
POS_INT_FIELD_MIN = 1
POS_INT_FIELD_MAX = 32767

CHAR_FIELD_MIN_LEN = 1

# Валидация Ingredient
INGREDIENT_NAME_MAX_LEN = 128
INGREDIENT_MEASUREMENT_UNIT_MAX_LEN = 64
INGREDIENTS_IN_RECIPE_MAX_NUM = 100

# Валидация Recipe
RECIPE_NAME_MAX_LEN = 256
RECIPE_SHORT_LINK_CODE_MAX_LEN = 6
SHORT_LINK_CODE_MAX_ATTEMPTS_GENERATE = 100

RECIPE_URL = '/recipes/{id}/'

# Валидация User
USER_EMAIL_MAX_LEN = 254
USER_USERNAME_MAX_LEN = 150
USER_FIRST_NAME_MAX_LEN = 150
USER_LAST_NAME_MAX_LEN = USER_FIRST_NAME_MAX_LEN

# Пагинация
PAGINATION_DEFAULT_PAGE_SIZE = 6
PAGINATION_MAX_PAGE_SIZE = 100

# Локализация: месяцы
MONTHS_IN_RUSSIAN_MAP = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}

# Локализация ошибок: общие
PAGE_NOT_FOUND_ERROR = 'Страница не найдена.'
RECIPE_NOT_FOUND_ERROR = 'Рецепт не найден.'
REQUIRED_FIELD_ERROR = 'Это поле обязательно.'

# Локализация ошибок: модель User
USER_USERNAME_ERROR = 'Никнейм не может быть пустым.'
USER_FIRST_NAME_ERROR = 'Имя не может быть пустым.'
USER_LAST_NAME_ERROR = 'Фамилия не может быть пустой.'

# Локализация ошибок: вьюсет User
INCORRECT_CURRENT_PASSWORD_ERROR = 'Неверный текущий пароль.'
SUBSCRIBE_TO_YOURSELF_ERROR = 'Нельзя подписаться на самого себя.'
ALREADY_SUBSCRIBED_ERROR = 'Вы уже подписаны.'
NOT_SUBSCRIBED_ERROR = 'Вы не были подписаны.'

# Локализация ошибок: модель Recipe
GENERATE_SHORT_LINK_ERROR = (
    'Произошла ошибка при генерации короткой ссылки. '
    'Пожалуйста, попробуйте позже.'
)

# Локализация ошибок: сериализатор Recipe
ZERO_INGREDIENTS_IN_RECIPE_ERROR = 'Нужен хотя бы один ингредиент.'
MAX_NUM_INGREDIENTS_IN_RECIPE_ERROR = (
    f'Максимум {INGREDIENTS_IN_RECIPE_MAX_NUM} ингредиентов.'
)
INGREDIENTS_IN_RECIPE_NOT_MAP_ERROR = 'Ингредиенты должны быть словарями.'
REPEATING_INGREDIENTS_IN_RECIPE_ERROR = 'Ингредиенты не должны повторяться.'
INGREDIENT_IN_RECIPE_NOT_FOUND = 'Ингредиент с id={id} не найден.'
MIN_MAX_INGREDIENTS_IN_RECIPE_ERROR = (
    f'Количество должно быть от '
    f'{POS_INT_FIELD_MIN} до {POS_INT_FIELD_MAX}.'
)

# Локализация ошибок: вьюсет Recipe
RECIPE_ALREADY_EXISTS_ERROR = 'Рецепт уже добавлен.'
SHORT_LINK_PREFIX = '/s/{short_link_code}'
SHOPPING_CART_EMPTY_ERROR = 'Список покупок пуст.'

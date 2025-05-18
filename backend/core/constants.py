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

RECIPE_SHORT_LINK_REDIRECT_URL = 'http://localhost/recipes/{id}'

# Валидация User
USER_EMAIL_MAX_LEN = 254
USER_USERNAME_MAX_LEN = 150
USER_FIRST_NAME_MAX_LEN = 150
USER_LAST_NAME_MAX_LEN = USER_FIRST_NAME_MAX_LEN

# Пагинация
PAGINATION_DEFAULT_PAGE_SIZE = 6
PAGINATION_MAX_PAGE_SIZE = 100

# Локализация
MONTHS_IN_RUSSIAN_MAP = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}

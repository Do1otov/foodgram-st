import shortuuid

from core.constants import RECIPE_SHORT_LINK_CODE_MAX_LEN


def generate_short_link_code(length: int = RECIPE_SHORT_LINK_CODE_MAX_LEN) -> str:
    return shortuuid.ShortUUID().random(length=length)

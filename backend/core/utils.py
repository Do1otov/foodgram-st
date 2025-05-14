import base64
from django.core.files.base import ContentFile


def decode_base64_image(data: str, filename: str = 'filename'):
    if ';base64,' not in data:
        raise ValueError('Некорректный формат изображения')

    try:
        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        file = ContentFile(base64.b64decode(imgstr), name=f'{filename}.{ext}')
        return file
    except Exception as e:
        raise ValueError('Ошибка при декодировании изображения') from e

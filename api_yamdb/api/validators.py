from django.core.exceptions import ValidationError

from api_yamdb.settings import BANNED_SYMBOLS


def validate_username(name):
    if name == 'me':
        raise ValidationError(
            'Имя me запрещено'
        )
    for symbol in name:
        if symbol in BANNED_SYMBOLS:
            raise ValidationError(
                'Имя пользователя содержит недопустимый символ'
            )

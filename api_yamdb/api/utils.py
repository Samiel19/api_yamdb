from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='team62@practicum.com',
        recipient_list=[user.email],
        fail_silently=False,
    )

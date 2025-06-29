from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_email(email, confirmation_code):
    """Функция для отправки электронного письма с кодом подтверждения."""

    subject = 'Ваш код подтверждения'
    message = f'Ваш код подтверждения: {confirmation_code}'
    email_from = settings.EMAIL_FROM
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

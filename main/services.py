from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')

    print(ip)
    return ip


def validate_email_data(
    recipient: str,
    subject: str, 
    content: str,    
) -> dict[str: str]: 
    errors = {}
    if not recipient: 
        errors['recipient'] = f'Отсутствует email получателя:'
    else: 
        try:
            validate_email(recipient)
        except ValidationError as e: 
            errors['recipient'] = f'Неверный email получателя: {recipient}'
    if not subject: 
        errors['subject'] = 'Отсутствует тема письма'
    if not content: 
        errors['content'] = 'Отсутствует содержание письма'

    return errors
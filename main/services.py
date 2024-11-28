from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def get_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
    return ip or request.META.get('REMOTE_ADDR')


def validate_email_data(
    sender: str, 
    host: str, 
    recipient: str,
    password: str,
    subject: str, 
    content: str,    
) -> dict[str: str]: 
    errors = {}
    
    if not sender: 
        errors['sender'] = f'Укажите email отправителя: {sender}'
    else: 
        try:
            validate_email(sender)
        except ValidationError as e: 
            errors['sender'] = f'Неверный email отправителя: {sender}'
    if not host: 
        errors['host'] = 'Укажите host отправителя'
    if not password: 
        errors['password'] = 'Укажите пароль отправителя'
    if not recipient: 
        errors['recipient'] = f'Неверный email получателя: {recipient}'
    else: 
        try:
            validate_email(recipient)
        except ValidationError as e: 
            errors['recipient'] = f'Неверный email получателя: {recipient}'
    if not subject: 
        errors['subject'] = 'Укажите тему письма'
    if not content: 
        errors['content'] = 'Укажите содержание письма'

    return errors
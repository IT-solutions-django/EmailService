from django import forms
from django.core.mail import send_mail, get_connection
from django.core.exceptions import ValidationError
from smtplib import SMTPException, SMTPAuthenticationError, SMTPConnectError
from .models import IpAddress


class IpAddressForm(forms.ModelForm):
    class Meta:
        model = IpAddress
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        host = cleaned_data.get('host')

        connection = get_connection(
            host=host,
            port=587,
            username=email,
            password=password,
            use_tls=True,
            use_ssl=False,
        )

        try:
            send_mail(
                subject='Тестовое письмо',
                message='Проверка того, что указаны верные данные',
                from_email=email,
                recipient_list=[email],
                connection=connection,
            )
        except SMTPAuthenticationError as e: 
            raise ValidationError(f'Ошибка аутентификации: {e}')
        except SMTPConnectError as e: 
            raise ValidationError(f'Ошибка подключения: {e}')
        except SMTPException as e: 
            raise ValidationError(f'Ошибка: {e}')
        except Exception as e:
            raise ValidationError(f'Ошибка при обновлении данных: {e}')

        return cleaned_data

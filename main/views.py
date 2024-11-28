from django.http import QueryDict, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import IpAddress
from .tasks import send_email_task
from .services import (
    validate_email_data,
    get_ip,
)



@method_decorator(csrf_exempt, name='dispatch')
class SendEmailView(View): 
    @csrf_exempt
    def post(self, request): 
        data: QueryDict = request.POST

        ip = get_ip(request)
        if not ip: 
            return JsonResponse({
                'status': 'error', 
                'errors': 'IP-адрес не определён',
            })
        if not IpAddress.objects.filter(ip=ip).exists(): 
            return JsonResponse({
                'status': 'error', 
                'errors': f'Неверный IP-адрес: {ip}',
            })

        sender = data.get('sender')
        password = data.get('password')
        host = data.get('host')
        recipient = data.get('recipient') 
        subject = data.get('subject') 
        content = data.get('content')

        errors = validate_email_data(
            sender=sender, 
            host=host, 
            recipient=recipient,
            password=password,
            subject=subject, 
            content=content,
        )
        if errors: 
            return JsonResponse({
                'status': 'error', 
                'errors': errors,
            })

        send_email_task.delay(
            sender=sender, 
            host=host, 
            recipient=recipient,
            password=password,
            subject=subject, 
            content=content,
        )

        return JsonResponse({
            'status': 'ok'
        })
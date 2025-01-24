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

        ip = data.get('ip')
        if not ip: 
            return JsonResponse({
                'status': 'error', 
                'errors': 'IP-адрес не определён',
            }, status=400)
        server_ip = IpAddress.objects.filter(ip=ip).first()
        if not server_ip: 
            return JsonResponse({
                'status': 'error', 
                'errors': f'Неверный IP-адрес: {ip}',
            }, status=403)

        recipient = data.get('recipient') 
        subject = data.get('subject') 
        content = data.get('content')

        errors = validate_email_data(
            recipient=recipient,
            subject=subject, 
            content=content,
        )
        if errors: 
            return JsonResponse({
                'status': 'error', 
                'errors': errors,
            }, status=400)
        
        sender = server_ip.email
        host = server_ip.host 
        password = server_ip.password

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
        }, status=200)
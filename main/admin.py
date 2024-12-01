from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
import os
from .forms import IpAddressForm
from django.http import FileResponse, HttpResponse
from .models import (
    IpAddress,
)


@admin.register(IpAddress)
class IpAddressAdmin(admin.ModelAdmin): 
    list_display = ['email', 'ip', 'host']
    form = IpAddressForm
    change_list_template = 'main/ip_addresses_change_list.html'

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path('download-logs/', self.view_logs_file, name='download-logs'),
        ]
        return my_urls + urls
    
    def view_logs_file(self, request) -> FileResponse | HttpResponse:
        log_file_path = os.path.join('logs', 'logs.log')

        try:
            response = FileResponse(open(log_file_path, 'rb'))
            return response
        except FileNotFoundError:
            self.message_user(request, 'Файл не найден', level='error')
        except PermissionError:
            self.message_user(request, 'Ошибка доступа', level='error')
        except Exception: 
            self.message_user(request, 'Необработанное исключение', level='error')
        return redirect('admin:main_main_changelist')
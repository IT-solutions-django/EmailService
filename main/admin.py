from django.contrib import admin
from .models import (
    IpAddress,
)


@admin.register(IpAddress)
class IpAddressAdmin(admin.ModelAdmin): 
    list_display = ['email', 'ip']
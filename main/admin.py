from django.contrib import admin
from django.contrib import messages
from .exceptions import WrongEmailDataError
from .forms import IpAddressForm
from .models import (
    IpAddress,
)


@admin.register(IpAddress)
class IpAddressAdmin(admin.ModelAdmin): 
    list_display = ['email', 'ip', 'host']
    form = IpAddressForm
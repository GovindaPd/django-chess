from django.contrib import admin
from .models import TokenSenderTable, WithComputerToken

admin.site.register(TokenSenderTable)
admin.site.register(WithComputerToken)

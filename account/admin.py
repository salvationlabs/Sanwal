from django.contrib import admin

from .models import User, BillingAddress
# Register your models here.

admin.site.register(User)
admin.site.register(BillingAddress)
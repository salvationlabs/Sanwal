from django.contrib import admin

from .models import User, NewsLetter
# Register your models here.

admin.site.register(User)
admin.site.register(NewsLetter)
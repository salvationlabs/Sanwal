from django.contrib import admin

from .models import NewsLetter, BecomeSeller, BecomeSellerImage
# Register your models here.
admin.site.register(NewsLetter)
admin.site.register(BecomeSeller)
admin.site.register(BecomeSellerImage)

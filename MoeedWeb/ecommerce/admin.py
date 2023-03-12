from django.contrib import admin

from .models import Type, Category, Product, OrderItem, Order, Images

# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(OrderItem)
admin.site.register(Order)

class ImageAdmin (admin.ModelAdmin):
	list_display = ('item', 'image_tag')
admin.site.register(Images, ImageAdmin)
from django.contrib import admin
from django.utils.translation import gettext as _


from .models import Type, Category, Product, OrderItem, Order, Images, Material

# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Material)


# Image Model
class ImageInline (admin.TabularInline):
	model = Images
	fk_name = 'img'
	verbose_name_plural = _('image')

class ImageAdmin (admin.ModelAdmin):
	list_display = ('item', 'image_tag')
admin.site.register(Images, ImageAdmin)
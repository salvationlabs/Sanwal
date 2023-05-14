from django.contrib import admin
from django.utils.translation import gettext as _


from .models import Type, Category, Product, OrderItem, Order, Images, Material

# Register your models here.


admin.site.register(Category)
admin.site.register(Type)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Material)


# Image Model
class ImageInline (admin.TabularInline):
	model = Images
	fk_name = 'item'
	max_num = 5
	verbose_name_plural = _('image')

# Listing Model
class ProductAdmin (admin.ModelAdmin):
	inlines = [ImageInline]
	list_display = ('title', 'price', 'discount_price', 'description', 'type', 'category', 'material', 'time_created')
	list_filter = ('price', 'discount_price', 'category', 'type', 'material', 'time_created')
	empty_value_display = '-empty-'
	
	# @admin.action
	# def make_active (self, request, queryset):
	# 	queryset.update(active=True)
	# 	messages.success(request, "Selected Record(s) Marked as Active Successfully !!")

	# @admin.action
	# def make_inactive (self, request, queryset):
	# 	queryset.update(active=False)
	# 	messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!")

	# actions = ['make_active', 'make_inactive']
admin.site.register(Product, ProductAdmin)

class ImageAdmin (admin.ModelAdmin):
	list_display = ('item', 'image_tag')
admin.site.register(Images, ImageAdmin)
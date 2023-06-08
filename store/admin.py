from django.contrib import admin
from django.utils.translation import gettext as _

from .models import (Category, Images, Material, Order, OrderItem, Product,
                     SubCategory)

# Register your models here.


admin.site.register(OrderItem)
admin.site.register(Order)


# Category Admin Model
@admin.register(Category)
class CategoryAdmin (admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}


@admin.register(SubCategory)
class SubCategoryAdmin (admin.ModelAdmin):
	list_display = ['name', 'category', 'slug']
	prepopulated_fields = {'slug': ('name',)}


@admin.register(Material)
class MaterialAdmin (admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}


# Image Model
class ImageInline (admin.TabularInline):
	model = Images
	fk_name = 'item'
	max_num = 5
	verbose_name_plural = _('image')

# Listing Model
class ProductAdmin (admin.ModelAdmin):
	inlines = [ImageInline]
	list_display = ('title', 'price', 'slug', 'discount_price', 'in_stock', 'is_active', 'description', 'category', 'subcategory', 'material', 'time_created', 'updated')
	list_filter = ('price', 'discount_price', 'in_stock', 'is_active', 'category', 'subcategory', 'material', 'time_created')
	list_editable = ['price', 'discount_price', 'is_active', 'in_stock']
	prepopulated_fields = {'slug': ('title',)}
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
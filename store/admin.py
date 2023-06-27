from django.contrib import admin
from django.utils.translation import gettext as _
from mptt.admin import MPTTModelAdmin

from .models import (Category, Material, ProductMaterial, Product, ProductType, ProductSpecification, ProductSpecificationValue, Images)

# Register your models here.


# Category Model
class CategoryAdmin(MPTTModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


# Material Model
@admin.register(Material)
class MaterialAdmin (admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}


# Material Inline Model
class MaterialInline(admin.TabularInline):
	model = ProductMaterial
	fk_name = 'item'
	verbose_name = _("material")
	verbose_name_plural = _("materials")


# Product Specification Value Inline Model
class ProductSpecificationInline(admin.TabularInline):
	model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
	inlines = [
		ProductSpecificationInline,
	]


class ProductSpecificationValueInline(admin.TabularInline):
	model = ProductSpecificationValue



# Image Inline Model
class ImageInline (admin.TabularInline):
	model = Images
	fk_name = 'item'
	max_num = 5
	verbose_name_plural = _('image')

# Product Model
@admin.register(Product)
class ProductAdmin (admin.ModelAdmin):
	inlines = [
		MaterialInline,
		ProductSpecificationValueInline,
		ImageInline,
	]
	list_display = ('title', 'regular_price', 'slug', 'discount_price', 'in_stock', 'is_active', 'description', 'category', 'time_created', 'updated', 'image_tag')
	list_filter = ('regular_price', 'discount_price', 'in_stock', 'is_active', 'category', 'time_created')
	list_editable = ['regular_price', 'discount_price', 'is_active', 'in_stock']
	prepopulated_fields = {'slug': ('title',)}
	empty_value_display = '-empty-'
	
# 	# @admin.action
# 	# def make_active (self, request, queryset):
# 	# 	queryset.update(active=True)
# 	# 	messages.success(request, "Selected Record(s) Marked as Active Successfully !!")

# 	# @admin.action
# 	# def make_inactive (self, request, queryset):
# 	# 	queryset.update(active=False)
# 	# 	messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!")

# 	# actions = ['make_active', 'make_inactive']


# Image Model
class ImageAdmin (admin.ModelAdmin):
	list_display = ('item', 'image_tag')
	list_filter = ('item',)
admin.site.register(Images, ImageAdmin)
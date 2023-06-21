from django.conf import settings
from django.db import models
from django.core.files.storage import default_storage
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from PIL import Image as PillowImage


# Model Managers
class ProductManager(models.Manager):
	def get_queryset(self):
		return super(ProductManager, self).get_queryset().filter(is_active=True)

# Create your models here.


class Category (models.Model):
	name = models.CharField(max_length=124, db_index=True)
	slug = models.SlugField(max_length=255, unique=True)

	class Meta:
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('store:products-by-category', kwargs={
			'category_slug': self.slug
		})


class SubCategory (models.Model):
	name = models.CharField(max_length=124, db_index=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategory")
	slug = models.SlugField(max_length=255, unique=True)

	class Meta:
		verbose_name_plural = 'subcategories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('store:products-by-subcategory', kwargs={
			'subcategory_slug': self.slug,
			'category_slug': self.category.slug,
		})


class Material (models.Model):
	name = models.CharField(max_length=124, db_index=True)
	slug = models.SlugField(max_length=255, unique=True)

	class Meta:
		verbose_name_plural = 'materials'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('store:products-by-material', kwargs={
			'material_slug': self.slug
		})


class Product (models.Model):
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=124, unique=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	description = models.TextField(blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
	subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True, related_name="subcategory")
	material = models.ForeignKey(Material, on_delete=models.CASCADE, blank=True, null=True, related_name="material")
	is_active = models.BooleanField(default=True)
	in_stock = models.BooleanField(default=True)
	time_created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	slug = models.SlugField(max_length=255, unique=True)
	objects = models.Manager()
	products = ProductManager()

	class Meta:
		verbose_name_plural = 'Products'
		ordering = ('-time_created',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('store:product', kwargs={
			'slug': self.slug
		})

	def save (self, *args, **kwargs):
		if self.slug == '':
			value = self.title.replace(" ", "-")
			self.slug = slugify(value, allow_unicode=True)
		super().save(*args, **kwargs)

	# def get_add_to_cart_url(self):
	# 	return reverse('order:add-to-cart', kwargs={
	# 		'slug': self.slug
	# 	})

	# def get_remove_from_cart_url(self):
	# 	return reverse('order:remove-from-cart', kwargs={
	# 		'slug': self.slug
	# 	})


class Images (models.Model):
	def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/listing_<title>/<filename>
		return 'images/item_{0}/{1}'.format(instance.item.title, filename)
	image = models.ImageField(upload_to=user_directory_path, blank=True)
	item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='img')

	def __str__(self):
		return f"{self.item}"

	def image_tag(self):
		if self.image:
			return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
		else:
			return 'No image found'
	image_tag.short_description = 'Image'

	# def save(self, *args, **kwargs):
	# 	super().save(*args, **kwargs)
	# 	if self.image:
	# 		img = PillowImage.open(self.image.path)  # open image

	# 		# resize image
	# 		if img.height > 500 or img.width > 500:
	# 			output_size = (500, 500)
	# 			img.thumbnail(output_size)  # resize image
	# 			img.save(self.image.path)  # save it again and override the larger image

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if self.image:
			img = PillowImage.open(self.image)
			
			# Resize image
			if img.height > 500 or img.width > 500:
				output_size = (500, 500)
				img.thumbnail(output_size)
				
				# Save the resized image to S3
				with default_storage.open(self.image.name, 'wb') as f:
					img.save(f, 'JPEG')
		

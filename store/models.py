from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField
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
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
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

	# def save (self, *args, **kwargs):
	# 	value = self.title.replace(" ", "-")
	# 	self.slug = slugify(value, allow_unicode=True)
	# 	super().save(*args, **kwargs)

	def get_add_to_cart_url(self):
		return reverse('store:add-to-cart', kwargs={
			'slug': self.slug
		})

	def get_remove_from_cart_url(self):
		return reverse('store:remove-from-cart', kwargs={
			'slug': self.slug
		})


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

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if self.image:
			img = PillowImage.open(self.image.path)  # open image

			# resize image
			if img.height > 500 or img.width > 500:
				output_size = (500, 500)
				img.thumbnail(output_size)  # resize image
				img.save(self.image.path)  # save it again and override the larger image


class OrderItem (models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ordered = models.BooleanField(default=False)
	item = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return f"{self.quantity} of {self.item.title}"

	def get_total_item_price(self):
		return self.quantity * self.item.price

	def get_total_discount_price(self):
		return self.quantity * self.item.discount_price

	def get_amount_saved(self):
		return self.get_total_item_price() - self.get_total_discount_price()

	def get_final_price(self):
		if self.item.discount_price:
			return self.get_total_discount_price()
		return self.get_total_item_price()


class Order (models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)
	billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.user.username

	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		return total


class BillingAddress (models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	street_address = models.CharField(max_length=100)
	appartment_address = models.CharField(max_length=100, blank=True, null=True)
	country = CountryField()
	zip_code = models.CharField(max_length=100)

	def __str__(self):
		return self.user.username

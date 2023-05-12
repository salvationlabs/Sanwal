from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.utils.safestring import mark_safe

# Create your models here.


class Type (models.Model):
	name = models.CharField(max_length=124)

	def __str__(self):
		return self.name


class Category (models.Model):
	name = models.CharField(max_length=124)
	type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="typeCategory")

	def __str__(self):
		return self.name


class Material (models.Model):
	name = models.CharField(max_length=124)

	def __str__ (self):
		return self.name


class Product (models.Model):
	title = models.CharField(max_length=124, unique=True)
	price = models.FloatField()
	discount_price = models.FloatField(blank=True, null=True)
	description = models.TextField(blank=True)
	type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="productType")
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="productCategory")
	material = models.ForeignKey(Material, on_delete=models.CASCADE, blank=True, null=True, related_name="productMaterial")
	time_created = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(editable=False)

	def __str__(self):
		return self.title

	def get_absolute_url (self):
		return reverse('product', kwargs={
			'slug': self.slug
		})

	def save (self, *args, **kwargs):
		value = self.title.replace(" ", "-")
		self.slug = slugify(value, allow_unicode=True)
		super().save(*args, **kwargs)
	
	def get_add_to_cart_url(self):
		return reverse('add-to-cart', kwargs={
			'slug': self.slug
		})

	def get_remove_from_cart_url(self):
		return reverse('remove-from-cart', kwargs={
			'slug': self.slug
		})


class Images (models.Model):
	def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/listing_<title>/<filename>
		return 'images/user_{0}/item_{1}/{2}'.format(instance.item.creator.username, instance.item.title, filename)
	image = models.ImageField(upload_to = user_directory_path, blank=True)
	item = models.ForeignKey(Product, on_delete= models.CASCADE, related_name='img')

	def __str__(self):
		return f"{self.item}"

	def image_tag (self):
		if self.image:
			return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
		else:
			return 'No image found'
	image_tag.short_description = 'Image'


class OrderItem (models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	ordered = models.BooleanField(default=False)
	item = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	def __str__ (self):
		return f"{self.quantity} of {self.item.title}"

	def get_total_item_price (self):
		return self.quantity * self.item.price

	def get_total_discount_price (self):
		return self.quantity * self.item.discount_price

	def get_amount_saved (self):
		return self.get_total_item_price() - self.get_total_discount_price()

	def get_final_price (self):
		if self.item.discount_price:
			return self.get_total_discount_price()
		return self.get_total_item_price()


class Order (models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)
	billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)

	def __str__ (self):
		return self.user.username

	def get_total (self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		return total


class BillingAddress (models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	street_address = models.CharField(max_length=100)
	appartment_address = models.CharField(max_length=100, blank=True, null=True)
	country = CountryField()
	zip_code = models.CharField(max_length=100)

	def __str__ (self):
		return self.user.username
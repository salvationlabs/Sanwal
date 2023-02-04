from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.


class Type (models.Model):
	name = models.CharField(max_length=124)

	def __str__(self):
		return self.name


class Category (models.Model):
	name = models.CharField(max_length=124)
	type = models.ForeignKey(Type, on_delete=models.CASCADE)

	def __str__(self):
		return self.name


class Product (models.Model):
	title = models.CharField(max_length=124)
	price = models.FloatField()
	discount_price = models.FloatField(blank=True, null=True)
	description = models.TextField(blank=True)
	type = models.ForeignKey(Type, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	time_created = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField()

	def __str__(self):
		return self.title

	def get_absolute_url (self):
		return reverse('product', kwargs={
			'slug': self.slug
		})
	
	def get_add_to_cart_url(self):
		return reverse('add-to-cart', kwargs={
			'slug': self.slug
		})

	def get_remove_from_cart_url(self):
		return reverse('remove-from-cart', kwargs={
			'slug': self.slug
		})


class OrderItem (models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	ordered = models.BooleanField(default=False)
	item = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	def __str__ (self):
		return f"{self.quantity} of {self.item.title}"


class Order (models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)

	def __str__ (self):
		return self.user.username
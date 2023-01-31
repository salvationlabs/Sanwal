from django.db import models

# Create your models here.


class Category (models.Model):
	name = models.CharField(max_length=124)

	def __str__(self):
		return f"{self.name}"


class Brand (models.Model):
	name = models.CharField(max_length=124)

	def __str__(self):
		return f"{self.name}"


class Product (models.Model):
	name = models.CharField(max_length=124)
	description = models.TextField(blank=True)
	is_digital = models.BooleanField(default=False)
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	time_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.name} | {self.time_created}"

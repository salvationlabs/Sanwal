from django.db import models

# Create your models here.

class NewsLetter(models.Model):
	email = models.EmailField()

	def __str__(self):
		return self.email


# class BecomeSeller(models.Model):


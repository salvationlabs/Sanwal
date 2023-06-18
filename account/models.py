from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class User(AbstractUser):
	class Meta:
		unique_together = ('email', )
		verbose_name = 'Accounts'
		verbose_name_plural = 'Accounts'

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	email = models.EmailField(unique=True)

	def email_user(self, subject, message):
		send_mail(
			subject,
			message,
			'talhamalik201532@gmail.com',
			[self.email],
			fail_silently=False,
		)

	def __str__(self):
		return self.email


class BillingAddress (models.Model):
	# User
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	# Delivery Details
	phone_number = models.CharField(max_length=15)
	address_line_1 = models.CharField(max_length=150)
	address_line_2 = models.CharField(max_length=150, blank=True)
	town_city = models.CharField(max_length=150)
	country = CountryField()
	zip_code = models.CharField(max_length=12, blank=True)

	def __str__(self):
		return self.user.username
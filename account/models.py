from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class User(AbstractUser):
	class Meta:
		unique_together = ('email', )
		verbose_name = 'Account'
		verbose_name_plural = 'Accounts'

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

	email = models.EmailField(unique=True)
	is_verified = models.BooleanField(default=False)

	def send_verification_email(self, subject, message, **kwargs):
		"""
        Send an email to this User.
        """
		from_email = 'talhamalik25.tm@gmail.com'
		# Create a plain text version of the email
		text_message = strip_tags(message)

		# Create the EmailMultiAlternatives object
		email = EmailMultiAlternatives(
			subject=subject, body=message, to=[self.email], from_email=from_email, **kwargs
		)
		email.attach_alternative(message, "text/html")


		email.send()
		# send_mail(
		# 	subject,
		# 	message,
		# 	'talhamalik25.tm@gmail.com',
		# 	[self.email],
		# 	fail_silently=False,
		# )

	def __str__(self):
		return self.email


class BillingAddress (models.Model):
	# User
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	# Delivery Details
	phone_number = models.CharField(max_length=15)
	address_line_1 = models.CharField(max_length=150)
	address_line_2 = models.CharField(max_length=150, blank=True)
	city = models.CharField(max_length=150)
	state = models.CharField(max_length=150)
	country = CountryField(blank_label='Country')
	zip_code = models.CharField(max_length=12, blank=True)

	class Meta:
		verbose_name = 'Billing Address'
		verbose_name_plural = 'Billing Addresses'

	def __str__(self):
		return self.user.username
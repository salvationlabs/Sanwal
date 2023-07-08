from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class NewsLetter(models.Model):
	email = models.EmailField()

	def __str__(self):
		return self.email


class BusinessOperation(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class BecomeSeller(models.Model):
	OPERATION_CHOICES = [
		('E/W', 'East/West'),
		('EX', 'Export'),
		('ONL', 'Online'),
		('RE', 'Retail'),
		('RB', 'Retail Brand'),
		('WS', 'Wholesale'),
	]
	CATEGORY = [
		('KDS', 'Kids'),
		('MR', 'Manufacturer'),
		('MN', 'Men'),
		('SME', 'SME'),
		('WMN', 'Women'),
	]
	SIZE_RANGE = [
		('1', '1-9'),
		('2', '10-19'),
		('3', '20-49'),
		('4', '50-99'),
		('5', '100-199'),
		('6', '200+'),
	]
	SUPPLY_CHAIN_CHOICES = [
		('IH', 'In-House (Self Production)'),
		('O', 'Outsourced'),
	]
	INVENTORY_CHOICES = [
		('YES', 'Yes, Ready to Ship'),
		('NO', 'No, Made to Order'),
		('BTH', 'Both'),
	]
	brand_name = models.CharField(verbose_name=_('Brand Name'), max_length=255)
	authorized_person_name = models.CharField(verbose_name=_('Authorized Person Name'), max_length=255)
	authorized_person_email = models.CharField(verbose_name=_('Authorized Person Email'), max_length=255)
	authorized_person_tel = models.CharField(verbose_name=_('Authorized Person Contact Phone/Mobile Number'), max_length=255)
	city = models.CharField(_("City"), max_length=150, help_text=_('In which city does the Brand proudly conduct its operations?'))
	website = models.URLField(verbose_name=_('Do you have any Website?'), max_length=255, blank=True)
	bussiness_operations = models.ManyToManyField(BusinessOperation, max_length=12, verbose_name=_('Brand\'s Business Operations'), help_text=_("If applicable, you may select multiple options"))
	products_category = models.CharField(choices=CATEGORY, max_length=12, verbose_name=_("Products Category"))
	catalogue_size = models.CharField(choices=SIZE_RANGE, max_length=12, verbose_name=_("Catalogue Size"), help_text=_('Number of products that you sell'))
	retail_price = models.DecimalField(verbose_name=_("Retail Price"), max_digits=10, decimal_places=2, help_text=_("Maximum 99999999.99"), error_messages={
		"name": {
			"max_length": _("The price must be between 0 and 99999999.99."),
		},
	})
	supply_chain = models.CharField(choices=SUPPLY_CHAIN_CHOICES, max_length=12, verbose_name=_("How do you manage your Supply Chain?"), help_text=_('Inhouse: Select this if you own machines/setup\nOutsourced: Select this if you do not own machines/setup and buy services from 3rd party vendors. '))
	inventory = models.CharField(choices=INVENTORY_CHOICES, max_length=12, verbose_name=_("Do you produce inventory before selling?"))
	feedback = models.TextField(verbose_name=_("If any, please share your feedback regarding the form."), help_text=_("Please give a brief introduction of your company"))

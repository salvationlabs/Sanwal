from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_OPTIONS = (
	('S', 'Stripe'),
	('P', 'PayPal')
)


class CheckoutForm(forms.Form):
	street_address = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder': 'Enter Street Address',
		'autofocus': True
	}), label='')
	appartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
		'placeholder': 'Appartment or Suite'
	}), label='')
	country = CountryField(blank_label='Select Country').formfield(
		widget=CountrySelectWidget(attrs={
		'class': 'custom_select'
	}), label='')
	zip_code = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder': 'Zip Code'
	}), label='')
	same_billing_address = forms.BooleanField(widget=forms.CheckboxInput())
	save_info = forms.BooleanField(widget=forms.CheckboxInput())
	payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_OPTIONS)

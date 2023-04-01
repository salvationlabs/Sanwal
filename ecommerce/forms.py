from django import forms
from django.forms import ModelForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Product


PAYMENT_OPTIONS = (
	('C', 'Cash'),
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


class ProductForm (ModelForm):
	class Meta:
		model = Product
		fields = ('__all__')

		exclude = ('time_created', 'slug')

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
			'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price', 'min': 0}),
			'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Discount Price', 'min': 0}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'material': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
		}
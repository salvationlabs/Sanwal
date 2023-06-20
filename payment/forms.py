from django import forms

from account.models import User, BillingAddress

class BillingForm(forms.ModelForm):
	first_name = forms.CharField(
		label='First Name', min_length=4, max_length=50, widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'First Name',
			}
		)
	)
	last_name = forms.CharField(
		label='Last Name', min_length=4, max_length=50, widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Last Name',
			}
		)
	)
	email = forms.EmailField(
		label='Email', max_length=200, widget=forms.EmailInput(
			attrs={
				'class': 'form-control mb-3',
				'placeholder': 'email',
			}
		)
	)
	save_info = forms.BooleanField(
		label='Save this information for next time',
		required=False,
		initial=True,
		widget=forms.CheckboxInput()
	)
	PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
    ]
    
	payment_method = forms.ChoiceField(
		choices=PAYMENT_CHOICES,
		widget=forms.RadioSelect(attrs={
			'checked': 'checked',
	})
	)
	class Meta:
		model = BillingAddress
		fields = ('__all__')
		exclude = ('user',)

		labels = {
			'address_line_1': 'Address',
			'address_line_2': 'Address 2',
			'state': 'State/Province/Region',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['phone_number'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'Phone number',
			'autofocus': 'autofocus'
		})
		self.fields['address_line_1'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'Address',
			'autofocus': 'autofocus'
		})
		self.fields['address_line_2'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'Address 2'
		})
		self.fields['city'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'City'
		})
		self.fields['state'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'State'
		})
		self.fields['country'].widget.attrs.update({
			'class': 'form-select',
			'placeholder': 'Country'
		})
		self.fields['zip_code'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'Zip Code'
		})

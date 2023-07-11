from django import forms

from .models import BecomeSeller


class BecomeSellerForm (forms.ModelForm):
	class Meta:
		model = BecomeSeller
		fields = ('__all__')

		exclude = ('time_created',)

		# widgets = {
		# 	'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
		# 	'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price', 'min': 0}),
		# 	'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Discount Price', 'min': 0}),
        #     'type': forms.Select(attrs={'class': 'form-select'}),
        #     'category': forms.Select(attrs={'class': 'form-select'}),
        #     'subcategory': forms.Select(attrs={'class': 'form-select'}),
        #     'material': forms.Select(attrs={'class': 'form-select'}),
        #     'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
		# }

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field_name in self.fields:
			self.fields[field_name].widget.attrs.update({
				'class': 'form-control mb-3',
				'placeholder': field_name.replace('_', ' ').title()
			})

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import (AuthenticationForm, SetPasswordForm, PasswordResetForm)

from .models import User


class LoginForm(AuthenticationForm):

	username = forms.EmailField(widget=forms.EmailInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Email',
			'id': 'login-email'
		}
	))
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Password',
			'id': 'login-pwd',
		}
	))


class RegistrationForm(forms.ModelForm):
	username = forms.CharField(label='Enter Username', min_length=4, max_length=50, help_text='Required')
	email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'Sorry, you will need an email address'})
	password = forms.CharField(label='Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'email',)

	def clean_username(self):
		username = self.cleaned_data['username'].lower()
		r = User.objects.filter(username=username)
		if r.count():
			raise forms.ValidationError('Username already exists')
		return username

	def cleaned_password2(self):
		cd = self.cleaned_data
		if c['password'] != cd['password2']:
			raise forms.ValidationError('Passwords do not match.')
		return cd['password2']

	def cleaned_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError(
				'Please use another email, that is already taken or used.'
			)
		return email

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': 'Username'}
		)
		self.fields['email'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': 'Email', 'name': 'email'}
		)
		self.fields['password'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': 'Password'}
		)
		self.fields['password2'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': 'Confirm Password'}
		)


class PwdResetForm(PasswordResetForm):
	email = forms.EmailField(max_length=254, widget=forms.EmailInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Email',
			'id': 'form-email'
		}
	))

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			user = User.objects.get(email=email)
		except ObjectDoesNotExist:
			raise forms.ValidationError(
				'Unfortunately we can not find that email address.'
			)
		return email


class PwdResetConfirmForm(SetPasswordForm):
	new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'New Password',
			'id': 'form-newpass'
		}
	))
	new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Repeat Password',
			'id': 'form-newpass2'
		}
	))


class ProfileEditForm(forms.ModelForm):

	email = forms.EmailField(
		label='Account email', max_length=200, widget=forms.TextInput(
			attrs={
				'class': 'form-control mb-3',
				'placeholder': 'email',
				'id': 'form-email',
				'readonly': 'readonly'
			}
		)
	)
	username = forms.CharField(
		label='Username', min_length=4, max_length=50, widget=forms.TextInput(
			attrs={
				'class': 'form-control mb-3',
				'placeholder': 'Username',
				'id': 'form-username',
				'readonly': 'readonly'
			}
		)
	)
	first_name = forms.CharField(
		label='First Name', min_length=4, max_length=50, widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'First Name',
				'id': 'form-first-name'
			}
		)
	)
	last_name = forms.CharField(
		label='First Name', min_length=4, max_length=50, widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Last Name',
				'id': 'form-last-name'
			}
		)
	)

	class Meta:
		model = User
		fields = ('email', 'username', 'first_name', 'last_name')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].required = True
		self.fields['email'].required = True

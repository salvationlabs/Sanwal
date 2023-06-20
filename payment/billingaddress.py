

class Billing():
	"""
	A base billing class, providing some default behaviors that can be inherited or overrided, as necessary.
	"""

	def __init__(self, request):
		self.session = request.session
		billing_address = self.session.get('billing_address')

		if 'billing_address' not in request.session:
			billing_address = self.session['billing_address'] = {}
		self.billing_address = billing_address
		# print(self.billing_address)

	def add(self, bform, uid):
		"""
		Adding and updating the users billing session data
		"""
		self.billing_address[uid] = {
			'first_name': bform.cleaned_data['first_name'],
			'last_name': bform.cleaned_data['last_name'],
			'email': bform.cleaned_data['email'],
			'phone_number': bform.cleaned_data['phone_number'],
			'address_line_1': bform.cleaned_data['address_line_1'],
			'address_line_2': bform.cleaned_data['address_line_2'],
			'city': bform.cleaned_data['city'],
			'state': bform.cleaned_data['state'],
			'country': bform.cleaned_data['country'],
			'zip_code': bform.cleaned_data['zip_code'],
			'payment_method': bform.cleaned_data['payment_method'],
		}

		self.save()

	def exists(self):
		"""
		Returns true if session contains billing address else false
		"""
		if self.billing_address != {}:
			return True
		else:
			return False

	def save(self):
		self.session.modified = True

	def clear(self):
		del self.session['billing_address']
		self.save()
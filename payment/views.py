from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .billingaddress import Billing
from basket.basket import Basket
from .forms import BillingForm
from account.models import BillingAddress

# Create your views here.
@login_required
def BasketView(request):
	basket = Basket(request)
	basketqty = basket.__len__()
	if basketqty <= 0:
		messages.error(request, 'Your basket is empty.')
		return redirect('store:index')

	if request.POST:
		try:
			billing = BillingAddress.objects.get(user=request.user)
			bform = BillingForm(request.POST, instance=billing)
		except ObjectDoesNotExist:
			bform = BillingForm(request.POST)

		if bform.is_valid():
			if bform.cleaned_data['save_info']:
				billingsave = bform.save(commit=False)
				billingsave.user = request.user
				billingsave.save()
			billing_session = Billing(request)
			billing_session.add(bform, request.user.id)
			return HttpResponseRedirect(reverse('order:order-placement'))
		else:
			return render(request, 'payment/checkout.html', {
				'form': bform
			})
	try:
		billing = BillingAddress.objects.get(user=request.user)
		bform = BillingForm(instance=billing, initial={
			'first_name': request.user.first_name,
			'last_name': request.user.last_name,
			'email': request.user.email
		})
	except ObjectDoesNotExist:
		billing_session = Billing(request)
		if billing_session.exists():
			billing_address = billing_session.billing_address[str(request.user.id)]

			bform = BillingForm(initial={
				'first_name': request.user.first_name,
				'last_name': request.user.last_name,
				'email': request.user.email,
				'phone_number': billing_address['phone_number'],
				'address_line_1': billing_address['address_line_1'],
				'address_line_2': billing_address['address_line_2'],
				'city': billing_address['city'],
				'state': billing_address['state'],
				'country': billing_address['country'],
				'zip_code': billing_address['zip_code'],
			})
		else:
			bform = BillingForm(initial={
				'first_name': request.user.first_name,
				'last_name': request.user.last_name,
				'email': request.user.email
			})


	return render(request, 'payment/checkout.html', {
		'form': bform
	})

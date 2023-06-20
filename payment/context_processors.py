from .billingaddress import Billing


def billing_session(request):
	return {
		'billing_session': Billing(request)
	}
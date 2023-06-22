from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from .models import Order, OrderItem

from store.models import Product

from account.models import User, BillingAddress

from payment.billingaddress import Billing

from basket.basket import Basket

# Create your views here.
@login_required
def Order_placement(request):
	"""
	Orders and Orderitems are fetched from basket_session if exist, and are stored in actual order and orderitem models respectively. Then session is cleared.
	"""
	basket_session = Basket(request)
	basketqty = basket_session.__len__()
	if basketqty <= 0:
		messages.error(request, 'Your basket is empty.')
		return redirect('store:index')
	billing_session = Billing(request)
	billing_address = billing_session.billing_address[str(request.user.id)]


	order = Order.objects.create(user=request.user, total_payment=basket_session.get_total_price())
	for item in basket_session:
		prdt = get_object_or_404(Product, id=item['product'].id)
		order_item = OrderItem.objects.create(item=prdt, user=request.user, quantity=item['qty'])
		order.items.add(order_item)
	
	try:
		billing_instance = BillingAddress.objects.get(user=request.user)
		order.billing_address = billing_instance
	except ObjectDoesNotExist:
		order.phone_number = billing_address['phone_number']
		order.address_line_1 = billing_address['address_line_1']
		order.address_line_2 = billing_address['address_line_2']
		order.city = billing_address['city']
		order.state = billing_address['state']
		order.country = billing_address['country']
		order.zip_code = billing_address['zip_code']
	
	order.first_name = billing_address['first_name']
	order.last_name = billing_address['last_name']
	order.email = billing_address['email']

	order.save()

	basket_session.clear()

	messages.success(request, "Thanks for shopping! Your order has been placed successfully.")
	return redirect('store:index')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order_item.quantity = 1
            order_item.save()
            order.items.remove(order_item)
            messages.success(request, f"{order_item.item.title} item was removed from your cart.")
        else:
            # add a message saying the user doesn't have an order
            messages.error(request, "This item was not in your cart.")
            return redirect('order:product', slug=slug)

    else:
        # add a message saying the user doesn't have an order
        messages.error(request, "You do not have an active order.")
        return redirect('order:product', slug=slug)
    return redirect('order:order-summary')


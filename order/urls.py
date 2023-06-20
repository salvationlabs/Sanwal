from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
	path('remove-from-cart/<slug>', views.remove_from_cart, name='remove-from-cart'),
	path('remove-single-item-from-cart/<slug>', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
	path('order_placement', views.Order_placement, name='order-placement')
]
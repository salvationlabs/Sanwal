from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import Category, Type, Product, OrderItem, Order

# Create your views here.

class HomeView(ListView):
    model = Product
    template_name = 'ecommerce/index.html'

class ItemDetailView (DetailView):
    model = Product
    template_name = 'ecommerce/product.html'

def home(request):
    items = Product.objects.all()
    return render(request, 'ecommerce/index.html', {
        'items': items
    })

def products (request):
    items = Product.objects.all()

    return render(request, 'ecommerce/products.html', {
        'items': items
    })

def checkout (request):
    return render(request, 'ecommerce/checkout.html')

def add_to_cart (request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "This item quantity was updated.")
        else:
            messages.success(request, "This item was added to your cart.")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, "This item was added to your cart.")
    return redirect('product', slug=slug)

def remove_from_cart (request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.success(request, "This item was removed from your cart.")
        else:
            # add a message saying the user doesn't have an order
            messages.error(request, "This item was not in your cart.")
            return redirect('product', slug=slug)

    else:
        # add a message saying the user doesn't have an order
        messages.error(request, "You do not have an active order.")
        return redirect('product', slug=slug)
    return redirect('product', slug=slug)

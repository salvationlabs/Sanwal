from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Category, Type, Product, OrderItem, Order, BillingAddress, Images
from .forms import CheckoutForm, ProductForm

# Create your views here.


class HomeView(ListView):
    model = Product
    paginate_by = 8
    template_name = 'ecommerce/index.html'

    def get_queryset(self, **kwargs):
       return Product.objects.all().order_by("-time_created")


class ItemTypeListView (ListView):
    model = Product
    paginate_by = 12
    template_name = 'ecommerce/products.html'

    def get_queryset(self, **kwargs):
       qs = super().get_queryset(**kwargs)
       return qs.filter(type__name=self.kwargs['type']).order_by("-time_created").all()


class ItemCategoryListView (ListView):
    model = Product
    paginate_by = 12
    template_name = 'ecommerce/products.html'

    def get_queryset(self, **kwargs):
       qs = super().get_queryset(**kwargs)
       return qs.filter(type__name=self.kwargs['type'], category__name=self.kwargs['category']).order_by("-time_created").all()


class ItemDetailView (DetailView):
    model = Product
    template_name = 'ecommerce/product.html'


class OrderSummaryView (LoginRequiredMixin, View):
    def get (self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect('/')
        return render(self.request, 'ecommerce/order_summary.html', {
            'object': order
        })


class CheckoutView (View):
    def get (self, *args, **kargs):
        # form
        form = CheckoutForm()
        return render(self.request, 'ecommerce/checkout.html', {
            'checkoutForm': form
        })
    def post (self, *args, **kargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=form.cleaned_data.get('street_address'),
                    appartment_address=form.cleaned_data.get('appartment_address'),
                    country=form.cleaned_data.get('country'),
                    zip_code=form.cleaned_data.get('zip_code')
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('checkout')
            messages.error(self.request, 'Failed Checkout')
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order.')
            return redirect('order-summary')


class PaymentView (View):
    def get (self, *args, **kargs):
        return render(self.request, 'ecommerce/payment.html')


@login_required
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
    return redirect('order-summary')


@login_required
def remove_from_cart (request, slug):
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
            return redirect('product', slug=slug)

    else:
        # add a message saying the user doesn't have an order
        messages.error(request, "You do not have an active order.")
        return redirect('product', slug=slug)
    return redirect('order-summary')


@login_required
def remove_single_item_from_cart (request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.success(request, f"{order_item.item.title} item quantity was updated.")
            else:
                order.items.remove(order_item)
                messages.success(request, f"{order_item.item.title} item has been removed.")
        else:
            # add a message saying the user doesn't have an order
            messages.error(request, "This item was not in your cart.")
            return redirect('product', slug=slug)

    else:
        # add a message saying the user doesn't have an order
        messages.error(request, "You do not have an active order.")
        return redirect('product', slug=slug)
    return redirect('order-summary')


@staff_member_required
def create_product(request):
    if request.method == "POST":
        product_form = ProductForm (request.POST)
        images = request.FILES.getlist('images')
        # image_form = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())

        if product_form.is_valid():
            product_obj = product_form.save(commit=False)
            product_obj.creator = request.user
            product_obj.save()

            for img in images:
                Images.objects.create(item=product_obj, image=img)

            messages.success(request, "Yeew, check it out on the home page!")
            return redirect("index")
        
        else:
                # messages.error(request, "Form is invalid. Please recheck the fields or fields\' values")
            for field in product_form:
                for error in field.errors:
                    messages.error(request, f"{field.name}: {error}")
                        
            print(product_form.errors)
            return render(
                request, 'ecommerce/createProduct.html', {
                    'product_form': product_form
                })

    product_form = ProductForm()
    return render(request, 'ecommerce/createProduct.html', {
        'product_form': product_form,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {username}')
            return redirect("index")
        else:
            messages.warning(request, "Invalid username and/or password.")
            # return redirect('')
    return render(request, "ecommerce/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.warning(request, "Passwords must match.")
            return render(request, "ecommerce/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "ecommerce/register.html")
        login(request, user)
        return redirect("index")
    else:
        return render(request, "ecommerce/register.html")
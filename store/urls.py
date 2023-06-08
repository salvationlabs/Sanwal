from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
	# Home Url
	path('', views.HomeView.as_view(), name='index'),
	# Category Url
	path('?category=<slug:category_slug>', views.CategoryListView.as_view(), name='products-by-category'),
	# SubCategory Url
	path('?category=<slug:category_slug>?subcategory=<slug:subcategory_slug>', views.SubCategoryListView.as_view(), name='products-by-subcategory'),
	# Material Url
	path('?material=<slug:material_slug>', views.MaterialListView.as_view(), name='products-by-material'),
	# Create Product Url
	path('create-product', views.create_product, name='create-product'),
	path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
	path('checkout/', views.CheckoutView.as_view(), name='checkout'),
	path('<slug>', views.ItemDetailView.as_view(), name='product'),
	path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
	path('remove-from-cart/<slug>', views.remove_from_cart, name='remove-from-cart'),
	path('remove-single-item-from-cart/<slug>', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
	path('payment/<payment_option>',  views.PaymentView.as_view(), name='payment'),
	path("login", views.login_view, name="login"),
	path("logout", views.logout_view, name="logout"),
	path("register", views.register, name="register"),
]

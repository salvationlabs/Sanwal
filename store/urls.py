from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
	# Home Url
	path('', views.HomeView.as_view(), name='index'),
	# Category Url
	path('?category=<slug:category_slug>', views.CategoryListView.as_view(), name='products-by-category'),
	# Material Url
	path('?material=<slug:material_slug>', views.MaterialListView.as_view(), name='products-by-material'),
	# Material Url
	path('?brands', views.BrandsListView.as_view(), name='products-by-brands'),
	# Create Product Url
	path('create-product/', views.create_product, name='create-product'),
	path('?product=<slug>', views.ItemDetailView.as_view(), name='product'),
]

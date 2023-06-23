from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
	# Home Url
	path('', views.HomeView.as_view(), name='index'),
	path('extra', views.ExtraView, name='extra'),
	# Category Url
	path('?category=<slug:category_slug>', views.CategoryListView.as_view(), name='products-by-category'),
	# SubCategory Url
	path('?category=<slug:category_slug>?subcategory=<slug:subcategory_slug>', views.SubCategoryListView.as_view(), name='products-by-subcategory'),
	# Material Url
	path('?material=<slug:material_slug>', views.MaterialListView.as_view(), name='products-by-material'),
	# Create Product Url
	path('create-product/', views.create_product, name='create-product'),
	path('?product=<slug>', views.ItemDetailView.as_view(), name='product'),
]

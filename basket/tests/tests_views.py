from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, SubCategory, Material, Product


class TestBasketView(TestCase):
	def setUp(self):
		# self.c = Client()

		User.objects.create(username='admin')  # user
		Category.objects.create(name='django', slug='django')  # category
		SubCategory.objects.create(name='django subcategory', category_id=1, slug='django-subcategory')  # subcategory
		Material.objects.create(name='python', slug='python')  # material

		Product.objects.create(category_id=1, subcategory_id=1, material_id=1, title='django beginners', creator_id=1, slug='django-beginners', price=20.00, discount_price=18.5, description='django description')

		Product.objects.create(category_id=1, subcategory_id=1, material_id=1, title='django intermediate', creator_id=1, slug='django-intermediate', price=500.00, discount_price=470.5, description='django description')

		Product.objects.create(category_id=1, subcategory_id=1, material_id=1, title='django advanced', creator_id=1, slug='django-advanced', price=120.00, discount_price=110.1, description='django description')

		self.client.post(
			reverse('basket:basket_update'), {
				'productId': 1,
				'product_qty': 2,
				'action': 'add',

			}, xhr=True
		)

		self.client.post(
			reverse('basket:basket_update'), {
				'productId': 2,
				'product_qty': 1,
				'action': 'add',
				
			}, xhr=True
		)

	def test_basket_url(self):
		"""
		Test Homepage response status
		"""
		response = self.client.get(reverse('basket:basket_summary'))
		self.assertEqual(response.status_code, 200)

	def test_basket_add(self):
		"""
		Test adding items in basket
		"""
		response = self.client.post(
			reverse('basket:basket_update'), {
				'productId': 3,
				'product_qty': 4,
				'action': 'add',
			}, xhr=True
		)

		self.assertEqual(response.json(), {'qty': 7, 'subtotal': 1020.0})

		response = self.client.post(
			reverse('basket:basket_update'), {
				'productId': 2,
				'product_qty': 2,
				'action': 'add',
				
			}, xhr=True
		)
		self.assertEqual(response.json(), {'qty': 9, 'subtotal': 2020.0})

	def test_basket_del(self):
		"""
		Test deleting items from the basket
		"""
		response = self.client.post(
			reverse('basket:basket_update'), {
				'productId': 2,
				'action': 'delete'
			}, xhr=True
		)
		self.assertEqual(response.json(), {'qty': 2, 'subtotal': 40.0})

	def test_basket_update(self):
		"""
		Test updating items in the basket
		"""
		response = self.client.post(
			reverse('basket:basket_update'), {
				'productId': 2,
				'product_qty': 3,
				'action': 'update'
			}, xhr=True
		)
		self.assertEqual(response.json(), {'qty': 5, 'subtotal': 1540.0})
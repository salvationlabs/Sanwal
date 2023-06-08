from django.contrib.auth.models import User
from django.test import TestCase

from store.models import (Category, Material, Product, SubCategory)


class TestCategoriesModel (TestCase):
	def setUp(self):
		self.data1 = Category.objects.create(name='django', slug='django')

	def test_category_model_entry(self):
		"""
		Test Category Model Data insertion/types/fields attributes
		"""
		data = self.data1
		self.assertTrue(isinstance(data, Category))

	def test_category_model_entry(self):
		"""
		Test Category Model Default Name
		"""
		data = self.data1
		self.assertEqual(str(data), 'django')


class TestProductsModel (TestCase):
	def setUp(self):
		Category.objects.create(name='django', slug='django')
		SubCategory.objects.create(name='django subcategory', category_id=1, slug='django-subcategory')
		Material.objects.create(name='python', slug='python')
		User.objects.create(username='admin')
		self.data1 = Product.objects.create(category_id=1, subcategory_id=1, material_id=1, title='django beginners', creator_id=1, slug='django-beginners', price=20.00, discount_price=18.5, description='django description')

	def test_product_model_entry(self):
		"""
		Test Product Model Data insertion/types/fields attributes
		"""
		data = self.data1
		self.assertTrue(isinstance(data, Product))
		self.assertEqual(str(data), 'django beginners')

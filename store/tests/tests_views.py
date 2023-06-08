from unittest import skip

from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Material, SubCategory
from store.views import HomeView, SubCategoryListView

# Test skip example
# @skip("demonstrating skipping")
# class TestSkip(TestCase):
#	def test_skip_example(self):
# 		pass


class TestViewResponses(TestCase):
	def setUp(self):
		self.c = Client()
		self.factory = RequestFactory()

		User.objects.create(username='admin')  # user
		Category.objects.create(name='django', slug='django')  # category
		SubCategory.objects.create(name='django subcategory', category_id=1, slug='django-subcategory')  # subcategory
		Material.objects.create(name='python', slug='python')  # material

	def test_url_allowed_hosts(self):
		"""
		Test allowed hosts
		"""
		response = self.c.get('/')
		self.assertEqual(response.status_code, 200)

	def test_product_category_detail_url(self):
		response = self.c.get(reverse('store:products-by-category', args={
			'category_slug': 'django'
		}))

		self.assertEqual(response.status_code, 200)

	def test_product_sub_category_detail_url(self):
		response = self.c.get(reverse('store:products-by-subcategory', args={
			'category_slug': 'django',
			'subcategory_slug': 'django-subcategory'
		}))

		self.assertEqual(response.status_code, 200)

	def test_product_material_detail_url(self):
		response = self.c.get(reverse('store:products-by-material', args={
			'material_slug': 'python'
		}))

		self.assertEqual(response.status_code, 200)

	def test_url_allowed_hosts(self):
		"""
		Test allowed Hosts
		"""
		response = self.c.get('/', HTTP_HOST='noaddress.com')
		self.assertEqual(response.status_code, 400)

		response = self.c.get('/', HTTP_HOST='sanwal.org')
		self.assertEqual(response.status_code, 200)

	def test_homepage_url(self):
		request = self.factory.get('/')
		response = HomeView.as_view()(request)
		response.render()

		html = response.content.decode('utf-8')
		# print(html)

		self.assertIn('<title>Sanwal: Your Ecommerce Store</title>', html)
		self.assertEqual(response.status_code, 200)

	def test_view_function(self):
		request = self.factory.get('/django/django-subcategory')
		response = SubCategoryListView.as_view()(request, category_slug='django', subcategory_slug='django-subcategory')

		self.assertEqual(response.status_code, 200)

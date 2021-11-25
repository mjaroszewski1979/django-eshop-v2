from django.db.models.query import QuerySet
from django.db import models
from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import search, product, category
from product.models import Product, Category



class ProductTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_search_url_is_resolved(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, search)

    def test_search_get(self):
        response = self.client.get(reverse('search'))
        self.assertContains(response, 'Search | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'product/search.html')

    def test_search_context(self):
        response = self.client.get(reverse('search'))
        self.assertIsNotNone(response.context['products'])
        self.assertIsNotNone(response.context['query'])
        self.assertIsInstance(response.context['products'], QuerySet)
        self.assertIsInstance(response.context['query'], str)

    def test_category_url_is_resolved(self):
        new_category = Category.objects.create(title='shoes', slug='shoes')
        url = reverse('category', args=(new_category.slug, ))
        self.assertEquals(resolve(url).func, category)

    def test_category_get(self):
        new_category = Category.objects.create(title='shoes', slug='shoes')
        response = self.client.get(reverse('category', args=(new_category.slug, )))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/category.html')

    def test_category_context(self):
        new_category = Category.objects.create(title='shoes', slug='shoes')
        response = self.client.get(reverse('category', args=(new_category.slug, )))
        self.assertIsNotNone(response.context['category'])
        self.assertEquals(response.context['category'], new_category)

from django.db.models.query import QuerySet
from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import frontpage, contact
from product.models import Product

class CoreTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_frontpage_url_is_resolved(self):
        url = reverse('frontpage')
        self.assertEquals(resolve(url).func, frontpage)

    def test_frontpage_get(self):
        response = self.client.get(reverse('frontpage'))
        self.assertContains(response, 'Welcome | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'core/frontpage.html')

    def test_frontpage_context(self):
        response = self.client.get(reverse('frontpage'))
        newest_products = Product.objects.all()[0:8]
        self.assertEquals(type(response.context['newest_products']), type(newest_products))
        self.assertIsNotNone(response.context['newest_products'])
        self.assertIsInstance(response.context['newest_products'], QuerySet)

    def test_contact_url_is_resolved(self):
        url = reverse('contact')
        self.assertEquals(resolve(url).func, contact)

    def test_contact_get(self):
        response = self.client.get(reverse('contact'))
        self.assertContains(response, 'Contact | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'core/contact.html')

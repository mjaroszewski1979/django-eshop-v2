from django.db.models.query import QuerySet
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.shortcuts import get_object_or_404
from .views import search, product, category
from product.models import Product, Category
from django.contrib.auth.forms import UserCreationForm
from vendor.models import Vendor
from django.db.models import Q
from .forms import AddToCartForm
from cart.cart import Cart





class ProductTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.new_category = Category.objects.create(title='shoes', slug='shoes')
        self.new_category.save()
        self.credentials={
            'username' : 'maciej',
            'password1' : 'jaroszewski123',
            'password2' : 'jaroszewski123'
        }
        self.form = UserCreationForm(self.credentials)
        self.user = self.form.save()
        self.new_vendor = Vendor.objects.create(name=self.user.username, created_by=self.user)
        self.pk = self.new_vendor.id
        self.new_vendor.save()
        self.vendor = Vendor.objects.get(id=self.pk)
        self.new_product = Product(
            category = self.new_category,
            vendor = self.vendor,
            title = 'nike',
            slug = 'nike',
            description = 'red snickers',
            price = 100
        )
        self.new_product.save()
        self.second_product = Product(
            category = self.new_category,
            vendor = self.vendor,
            title = 'adidas',
            slug = 'adidas',
            description = 'white snickers',
            price = 200
        )
        self.second_product.save()
        self.cart = Cart(self.client)
        

    def test_search_url_is_resolved(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, search)

    def test_search_get(self):
        response = self.client.get(reverse('search'))
        self.assertContains(response, 'Search | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'product/search.html')

    def test_search_query(self):
       
        response = self.client.get('/products/search/?query=red')
        query = response.context['query']
        products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        products_title = products.get(vendor=self.vendor)
        context = response.context['products']
        context_title = context.get(vendor=self.vendor)
        self.assertEquals(query, 'red')
        self.assertEquals(products_title, context_title)

    def test_search_context(self):
        response = self.client.get(reverse('search'))
        self.assertIsNotNone(response.context['products'])
        self.assertIsNotNone(response.context['query'])
        self.assertIsInstance(response.context['products'], QuerySet)
        self.assertIsInstance(response.context['query'], str)

    def test_category_url_is_resolved(self):
        url = reverse('category', args=(self.new_category.slug, ))
        self.assertEquals(resolve(url).func, category)

    def test_category_get(self):
        response = self.client.get(reverse('category', args=(self.new_category.slug, )))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/category.html')

    def test_category_context(self):
        response = self.client.get(reverse('category', args=(self.new_category.slug, )))
        self.assertIsNotNone(response.context['category'])
        self.assertEquals(response.context['category'], self.new_category)

    def test_product_url_is_resolved(self):
        url = reverse('product',args= (self.new_category.slug, self.new_product.slug))
        self.assertEquals(resolve(url).func, product)

    def test_product_get(self):
        response = self.client.get(reverse('product', args= (self.new_category.slug, self.new_product.slug)))
        product = get_object_or_404(Product, category__slug=self.new_category.slug, slug=self.new_product.slug)
        similar_products = list(product.category.products.exclude(id=product.id))
        add_to_cart_form = AddToCartForm()
        self.assertContains(response, product.title, status_code=200)
        self.assertTemplateUsed(response, 'product/product.html')
        self.assertEquals(response.context['product'], product)
        self.assertEquals(similar_products[-1], self.second_product)
        self.assertEquals(response.context['similar_products'], similar_products)
        self.assertEquals(type(response.context['form']), type(add_to_cart_form))

    def test_product_post(self):
        data = {
            'quantity': 2
        }
        response = self.client.post(reverse('product', args= (self.new_category.slug, self.new_product.slug)), data, follow=True)
        self.assertContains(response, self.new_product.title, status_code=200)
        self.assertContains(response, 'The product was added to the cart')
        self.assertTemplateUsed(response, 'product/product.html')

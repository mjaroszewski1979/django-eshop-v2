# Python libraries
import io
from PIL import Image

# Django imports
from django.db.models.query import QuerySet
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.text import slugify

# App imports
from cart.views import cart_detail
from cart.forms import CheckoutForm
from cart.cart import Cart
from core.views import frontpage, contact
from order.models import Order, OrderItem
from product.models import Product, Category
from product.views import search, product, category
from product.forms import AddToCartForm
from vendor.models import Vendor
from vendor.views import become_vendor, vendor_admin, add_product, edit_vendor, vendors, vendor
from vendor.forms import ProductForm


# Global variables
user = ''
vendor_1 = ''
new_order = ''
new_vendor = ''
pk = ''
new_category = ''
cart = ''
data = ''
form = ''
new_product = ''
photo_file = ''
second_product = ''

# Function returns sample image for testing purposes
def generate_photo_file():
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

# Establishing fixtures to handle especially expensive setup operations for all of the tests within a module
def setUpModule():
    global cart, form, new_category, new_order, new_product, new_vendor, photo_file, pk, second_product, user, vendor_1

    client = Client()
    cart = Cart(client)
    new_category = Category.objects.create(title='shoes', slug='shoes')
    new_category.save()
    credentials={
        'username' : 'maciej',
        'password1' : 'jaroszewski123',
        'password2' : 'jaroszewski123'
    }
    form = UserCreationForm(credentials)
    user = form.save()
    new_vendor = Vendor.objects.create(name=user.username, created_by=user)
    pk =new_vendor.id
    new_vendor.save()
    vendor_1 = Vendor.objects.get(id=pk)
    new_product = Product(
        category =new_category,
        vendor = vendor_1,
        title = 'nike',
        slug = 'nike',
        description = 'red snickers',
        price = 100
    )
    new_product.save()
    second_product = Product(
            category = new_category,
            vendor = vendor_1,
            title = 'adidas',
            slug = 'adidas',
            description = 'white snickers',
            price = 200
        )
    second_product.save()
    new_order = Order(
        first_name = 'maciej',
        last_name = 'jaroszewski',
        email = 'maciej@gmail.com',
        address = 'poznan',
        zipcode = '1234567',
        place = 'poland',
        phone = '123456789',
        paid_amount = '100')
    new_order.save()
    new_order.vendors.add(vendor_1)
    photo_file = generate_photo_file()
    global data
    data = {
                'category': new_category,
                'image': photo_file,
                'title': 'nike',
                'description': 'nike',
                'price': 20
            }
    

# Testing cart app
class CartTest(TestCase):

    def test_cart_detail_url_is_resolved(self):
        url = reverse('cart')
        self.assertEquals(resolve(url).func, cart_detail)

    def test_cart_detail_get(self):
        response = self.client.get(reverse('cart'))
        self.assertContains(response, 'Cart | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'cart/cart.html')

    def test_cart_detail_context(self):
        response = self.client.get(reverse('cart'))
        stripe_pub_key = settings.STRIPE_PUB_KEY
        self.assertIsInstance(response.context['form'], CheckoutForm)
        self.assertEquals(response.context['stripe_pub_key'], stripe_pub_key)

    def test_cart_detail_post(self):
        response = self.client.post(reverse('cart'), {
            'first_name' : 'maciej',
            'last_name' : 'jaroszewski',
            'email' : 'maciej@gmail.com',
            'phone' : '555345121',
            'address' : 'poznan',
            'zipcode' : '61381',
            'place' : 'polska',
            'cardnumber' : '4242424242424242',
            'exp-date' : '1222',
            'cvc' : '123'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_checkoutform_valid_data(self):
        data = {
            'first_name' : 'maciej',
            'last_name' : 'jaroszewski',
            'email' : 'maciej@gmail.com',
            'phone' : '111222333',
            'address' : 'poznan',
            'zipcode' : '123456',
            'place' : 'poland',
            'stripe_token' : '123456789'
        }
        form = CheckoutForm(data)
        self.assertTrue(form.is_valid())

    def test_checkoutform_no_valid_data(self):
        data = {}
        form = CheckoutForm(data)
        self.assertFalse(form.is_valid())

# Testing core app
class CoreTest(TestCase):

    def test_frontpage_url_is_resolved(self):
        url = reverse('frontpage')
        self.assertEquals(resolve(url).func, frontpage)

    def test_frontpage_get(self):
        response = self.client.get(reverse('frontpage'))
        self.assertContains(response, 'Welcome | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'core/frontpage.html')

    def test_frontpage_context(self):
        response = self.client.get(reverse('frontpage'))
        newest_products = Product.objects.all()
        self.assertEquals(newest_products.count(), 2)
        self.assertEquals(str(response.context['newest_products']), str(newest_products))
        self.assertIsNotNone(response.context['newest_products'])
        self.assertIsInstance(response.context['newest_products'], QuerySet)

    def test_contact_url_is_resolved(self):
        url = reverse('contact')
        self.assertEquals(resolve(url).func, contact)

    def test_contact_get(self):
        response = self.client.get(reverse('contact'))
        self.assertContains(response, 'Contact | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'core/contact.html')

# Testing order app
class OrderTest(TestCase):

    def test_order_model(self):
        global new_order, pk

        orders = Order.objects.all()
        new_order_vendor = new_order.vendors.get(id=pk)
        order_print = str(Order.objects.get(id=new_order.id))
        self.assertIsNotNone(new_order)
        self.assertEquals(orders.count(), 1)
        self.assertEquals(vendor_1.name, new_order_vendor.name)
        self.assertEquals(order_print, new_order.first_name)

    def test_order_item_model(self):
        global new_category, new_order, user, vendor_1

        new_product = Product(
            category = new_category,
            vendor = vendor_1,
            title = 'nike',
            slug = 'nike',
            description = 'snickers',
            price = 100
        )
        new_product.save()

        new_order_item = OrderItem(
        order = new_order,
        product = new_product,
        vendor = vendor_1,
        vendor_paid = True,
        price = 200,
        quantity = 2
        )
        new_order_item.save()
        items = OrderItem.objects.all()
        new_order_item_print = str(OrderItem.objects.get(id=new_order_item.id))
        total = new_order_item.get_total_price()

        self.assertIsNotNone(new_order_item)
        self.assertEquals(items.count(), 1)
        self.assertEquals(new_order_item.order, new_order)
        self.assertEquals(new_order_item.product, new_product)
        self.assertEquals(new_order_item.vendor, vendor_1)
        self.assertEquals(new_order_item.vendor.name, user.username)
        self.assertEquals(new_order_item_print, str(new_order_item.id))
        self.assertEquals(total, 400)

# Testing product app
class ProductTest(TestCase):

    def test_search_url_is_resolved(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, search)

    def test_search_get(self):
        response = self.client.get(reverse('search'))
        self.assertContains(response, 'Search | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'product/search.html')

    def test_search_query(self):
        global vendor_1

        response = self.client.get('/products/search/?query=red')
        query = response.context['query']
        products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        products_title = products.get(vendor=vendor_1)
        context = response.context['products']
        context_title = context.get(vendor=vendor_1)
        self.assertEquals(query, 'red')
        self.assertEquals(products_title, context_title)

    def test_search_context(self):
        response = self.client.get(reverse('search'))
        self.assertIsNotNone(response.context['products'])
        self.assertIsNotNone(response.context['query'])
        self.assertIsInstance(response.context['products'], QuerySet)
        self.assertIsInstance(response.context['query'], str)

    def test_category_url_is_resolved(self):
        global new_category

        url = reverse('category', args=(new_category.slug, ))
        self.assertEquals(resolve(url).func, category)

    def test_category_get(self):
        global new_category

        response = self.client.get(reverse('category', args=(new_category.slug, )))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/category.html')

    def test_category_context(self):
        global new_category

        response = self.client.get(reverse('category', args=(new_category.slug, )))
        self.assertIsNotNone(response.context['category'])
        self.assertEquals(response.context['category'], new_category)

    def test_product_url_is_resolved(self):
        global new_category, new_product

        url = reverse('product',args= (new_category.slug, new_product.slug))
        self.assertEquals(resolve(url).func, product)

    def test_product_get(self):
        global new_category, second_product

        response = self.client.get(reverse('product', args= (new_category.slug, new_product.slug)))
        product = get_object_or_404(Product, category__slug=new_category.slug, slug=new_product.slug)
        similar_products = list(product.category.products.exclude(id=product.id))
        add_to_cart_form = AddToCartForm()
        self.assertContains(response, product.title, status_code=200)
        self.assertTemplateUsed(response, 'product/product.html')
        self.assertEquals(response.context['product'], product)
        self.assertEquals(similar_products[-1], second_product)
        self.assertEquals(response.context['similar_products'], similar_products)
        self.assertEquals(type(response.context['form']), type(add_to_cart_form))

    def test_product_post(self):
        global new_category, new_product

        data = {
            'quantity': 2
        }
        response = self.client.post(reverse('product', args= (new_category.slug, new_product.slug)), data, follow=True)
        self.assertContains(response, new_product.title, status_code=200)
        self.assertContains(response, 'The product was added to the cart')
        self.assertTemplateUsed(response, 'product/product.html')

# Testing vendor app
class VendorTest(TestCase):

    def setUp(self):
        self.client.login(username='maciej', password='jaroszewski123')

    def test_form_valid_data(self):
        global form
        self.assertTrue(form.is_valid())

    def test_form_no_valid_data(self):
        form = UserCreationForm(data={})
        self.assertFalse(form.is_valid())

    def test_become_vendor_url_is_resolved(self):
        url = reverse('become_vendor')
        self.assertEquals(resolve(url).func, become_vendor)

    def test_become_vendor_get(self):
        response = self.client.get(reverse('become_vendor'))
        form = UserCreationForm()
        self.assertContains(response, 'Become vendor | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'vendor/become_vendor.html') 
        self.assertIsNotNone(response.context['form'])
        self.assertEquals(type(response.context['form']), type(form))

    def test_become_vendor_post(self):
        data={
            'username' : 'maciej123',
            'password1' : 'jaroszewski',
            'password2' : 'jaroszewski'
        }
        response = self.client.post(reverse('become_vendor'), data, follow=True)
        self.assertContains(response, 'Welcome | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'core/frontpage.html')

    def test_vendors_url_is_resolved(self):
        url = reverse('vendors')
        self.assertEquals(resolve(url).func, vendors)

    def test_vendors_view(self):
        global new_vendor
        vendors = Vendor.objects.all()
        response = self.client.get(reverse('vendors'))
        self.assertContains(response, 'Vendors | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'vendor/vendors.html') 
        self.assertIsNotNone(response.context['vendors'])
        self.assertIsNotNone(new_vendor)
        self.assertEquals(vendors.count(), 1)

    def test_vendor_url_is_resolved(self):
        global pk
        url = reverse('vendor', args=(pk,))
        self.assertEquals(resolve(url).func, vendor)

    def test_vendor_view(self):
        global pk
        response = self.client.get(reverse('vendor', args=(pk,)))
        vendor = Vendor.objects.get(id=pk)
        self.assertContains(response, vendor.name , status_code=200)
        self.assertTemplateUsed(response, 'vendor/vendor.html') 
        self.assertIsNotNone(response.context['vendor'])
        self.assertEquals(type(response.context['vendor']), type(vendor))
        self.assertIsNotNone(vendor)

    def test_vendor_admin_url_is_resolved(self):
        url = reverse('vendor_admin')
        self.assertEquals(resolve(url).func, vendor_admin)

    def test_vendor_admin_view(self):
        global new_vendor
        response = self.client.get(reverse('vendor_admin'))
        self.assertContains(response, 'Vendor admin | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'vendor/vendor_admin.html')
        self.assertIsNotNone(response.context['vendor'])
        self.assertEquals(type(response.context['vendor']), type(new_vendor))

    def test_edit_vendor_url_is_resolved(self):
        url = reverse('edit_vendor')
        self.assertEquals(resolve(url).func, edit_vendor)

    def test_edit_vendor_get(self):
        global new_vendor
        response = self.client.get(reverse('edit_vendor'))
        self.assertContains(response, 'Edit vendor | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'vendor/edit_vendor.html')
        self.assertIsNotNone(response.context['vendor'])
        self.assertEquals(type(response.context['vendor']), type(new_vendor))

    def test_edit_vendor_post(self):
        data = {
            'name': 'maciej_new',
            'email': 'maciej@gmail.com'
        }
        response = self.client.post(reverse('edit_vendor'), data, follow=True)
        self.assertContains(response, 'Vendor admin | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'vendor/vendor_admin.html')

    def test_add_product_url_is_resolved(self):
        url = reverse('add_product')
        self.assertEquals(resolve(url).func, add_product)

    def test_add_product_get(self):
        form = ProductForm()
        response = self.client.get(reverse('add_product'))
        self.assertContains(response, 'Add product | URBAN STYLE', status_code=200)
        self.assertTemplateUsed(response, 'vendor/add_product.html')
        self.assertIsNotNone(response.context['form'])
        self.assertEquals(type(response.context['form']), type(form))

    def test_add_product_post(self):
        global data
        response = self.client.post(reverse('add_product'), data, format='multipart')
        self.assertEquals(response.status_code, 200)

    def test_add_product_form(self):
        global data, user
        product_form = ProductForm(data)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.vendor = user.vendor
            product.slug = slugify(product.title)
            product.save()
            products = Product.objects.all()

            self.assertIsNotNone(product)
            self.assertEquals(product.title, 'nike')
            self.assertEquals(product.slug, 'nike')
            self.assertEquals(product.price, 20)
            self.assertEquals(str(product.category), 'shoes')
            self.assertEquals(str(product.vendor), 'maciej')
            self.assertEquals(products.count(), 3)
        


    

   
        



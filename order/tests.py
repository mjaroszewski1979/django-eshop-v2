from django.test import TestCase
from .models import Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from vendor.models import Vendor
from product.models import Category, Product



class OrderTest(TestCase):

    def setUp(self):
        self.credentials={
            'username' : 'maciej',
            'password1' : 'jaroszewski123',
            'password2' : 'jaroszewski123'
        }
        self.form = UserCreationForm(self.credentials)
        self.user = self.form.save()
        self.new_vendor = Vendor.objects.create(name=self.user.username, created_by=self.user)
        self.pk=self.new_vendor.id
        self.new_vendor.save()
        self.vendor = Vendor.objects.get(id=self.pk)

        self.new_order = Order(
            first_name = 'maciej',
            last_name = 'jaroszewski',
            email = 'maciej@gmail.com',
            address = 'poznan',
            zipcode = '1234567',
            place = 'poland',
            phone = '123456789',
            paid_amount = '100')

        self.new_order.save()
        self.new_order.vendors.add(self.vendor)
        self.new_category = Category.objects.create(title='shoes', slug='shoes')

    def test_order_model(self):
        orders = Order.objects.all()
        new_order_vendor = self.new_order.vendors.get(id=self.pk)
        order_print = str(Order.objects.get(id=self.new_order.id))
        self.assertIsNotNone(self.new_order)
        self.assertEquals(orders.count(), 1)
        self.assertEquals(self.vendor.name, new_order_vendor.name)
        self.assertEquals(order_print, self.new_order.first_name)

    def test_order_item_model(self):
        new_product = Product(
            category = self.new_category,
            vendor = self.vendor,
            title = 'nike',
            slug = 'nike',
            description = 'snickers',
            price = 100
        )
        new_product.save()

        new_order_item = OrderItem(
        order = self.new_order,
        product = new_product,
        vendor = self.vendor,
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
        self.assertEquals(new_order_item.order, self.new_order)
        self.assertEquals(new_order_item.product, new_product)
        self.assertEquals(new_order_item.vendor, self.vendor)
        self.assertEquals(new_order_item.vendor.name, self.user.username)
        self.assertEquals(new_order_item_print, str(new_order_item.id))
        self.assertEquals(total, 400)

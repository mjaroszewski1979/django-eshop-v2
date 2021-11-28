from django.test import TestCase
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from vendor.models import Vendor

class OrderTest(TestCase):

    def test_order_model(self):
        credentials={
            'username' : 'maciej',
            'password1' : 'jaroszewski123',
            'password2' : 'jaroszewski123'
        }
        form = UserCreationForm(credentials)
        self.user = form.save()
        new_vendor = Vendor.objects.create(name=self.user.username, created_by=self.user)
        pk=new_vendor.id
        new_vendor.save()
        vendor = Vendor.objects.get(id=pk)

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
        new_order.vendors.add(vendor)
     
        orders = Order.objects.all()
        new_order_vendor = new_order.vendors.get(id=pk)
        self.assertIsNotNone(new_order)
        self.assertEquals(orders.count(), 1)
        self.assertEquals(vendor.name, new_order_vendor.name)

from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import cart_detail
from .forms import CheckoutForm
from django.conf import settings

class CartTest(TestCase):

    def setUp(self):
        self.client = Client()

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

    def test_cart_detail_post_no_items(self):
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
        })
        self.assertContains(response, "You don't have any products in your cart!", status_code=200)
        self.assertTemplateUsed(response, 'cart/cart.html')

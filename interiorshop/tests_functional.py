from selenium import webdriver
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, Client
from django.urls import reverse, resolve
from product.models import Product, Category
from django.contrib.auth.forms import UserCreationForm
from vendor.models import Vendor


class TestUrbanStyle(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('interiorshop/chromedriver.exe')
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
        self.client.force_login(self.user)
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
        

    def tearDown(self):
        self.browser.close()

    def test_frontpage_view_is_displayed(self):
        self.browser.get(self.live_server_url)

        alert_1 = self.browser.find_element_by_class_name('frontpage')
        self.assertEquals(
            alert_1.find_element_by_tag_name('h2').text,
            "NEWEST PRODUCTS"
        )
        alert_2 = self.browser.find_element_by_class_name('box')
        self.assertEquals(
            alert_2.find_element_by_tag_name('h3').text,
            (str(self.new_product.price) + '.00')
        )

    def test_frontpage_view_button(self):
        self.browser.get(self.live_server_url)
        button = self.browser.find_element_by_class_name('button-frontpage')
        button.click()
        product_url = self.live_server_url + reverse('product',args= (self.new_category.slug, self.new_product.slug))
        self.assertEquals(
            self.browser.current_url,
            product_url
        )

    def test_frontpage_category_button(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_class_name('category-item').click()
        category_url = self.live_server_url + reverse('category', args=(self.new_category.slug, ))
        self.assertEquals(
            self.browser.current_url,
            category_url
        )

    def test_frontpage_contact_button(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_class_name('contact-item').click()
        category_url = self.live_server_url + reverse('contact')
        self.assertEquals(
            self.browser.current_url,
            category_url
        )

    def test_frontpage_become_vendor_button(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_class_name('become-vendor').click()
        category_url = self.live_server_url + reverse('become_vendor')
        self.assertEquals(
            self.browser.current_url,
            category_url
        )
      
    def test_frontpage_vendors_button(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_class_name('vendors').click()
        category_url = self.live_server_url + reverse('vendors')
        self.assertEquals(
            self.browser.current_url,
            category_url
        )


      

    
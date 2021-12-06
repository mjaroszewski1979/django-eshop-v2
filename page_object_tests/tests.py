from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from . import page
from product.models import Product, Category
from django.contrib.auth.forms import UserCreationForm
from vendor.models import Vendor
from django.urls import reverse


class UrbanTest(StaticLiveServerTestCase):

    def setUp(self):
        self.driver =  webdriver.Chrome('selenium_tests/chromedriver.exe')
        
        self.driver.set_window_size(1920, 1080)
        self.new_category = Category.objects.create(title='shoes', slug='shoes')
        self.new_category.save()
        credentials={
        'username' : 'maciej',
        'password1' : 'jaroszewski123',
        'password2' : 'jaroszewski123'
    }
        self.form = UserCreationForm(credentials)
        self.user = self.form.save()
        self.new_vendor = Vendor.objects.create(name=self.user.username, created_by=self.user)
        self.pk =self.new_vendor.id
        self.new_vendor.save()
        self.vendor_1 = Vendor.objects.get(id=self.pk)
        self.new_product = Product(
            category = self.new_category,
            vendor = self.vendor_1,
            title = 'nike',
            slug = 'nike',
            description = 'red snickers',
            price = 100
        )
        self.new_product.save()


    def tearDown(self):
        self.driver.close()


    def test_frontpage(self):
        self.driver.get(self.live_server_url)
        main_page = page.MainPage(self.driver)
        assert main_page.is_title_matches()

        main_page.click_view_button()
        assert main_page.is_view_button_works(self.new_product.title)

        category_url = self.live_server_url + reverse('category', args=(self.new_category.slug, ))
        main_page.click_category_link()
        assert main_page.is_category_link_works(category_url)

        contact_url = self.live_server_url + reverse('contact')
        main_page.click_contact_link()
        assert main_page.is_contact_link_works(contact_url)

        become_vendor = self.live_server_url + reverse('become_vendor')
        main_page.click_become_vendor_link()
        assert main_page.is_become_vendor_link_works(become_vendor)

        vendors = self.live_server_url + reverse('vendors')
        main_page.click_vendors_link()
        assert main_page.is_vendors_link_works(vendors)
        
        main_page.execute_search()
        search_results_page = page.SearchResultsPage(self.driver)
        assert search_results_page.is_results_found()
    


    






























'''from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from product.models import Product, Category
from django.contrib.auth.forms import UserCreationForm
from vendor.models import Vendor
from .main import MainPage 


class UrbanTest(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('selenium_tests/chromedriver.exe')
        self.driver.set_window_size(1920, 1080)
        self.wait = W(self.driver, 5)
        self.new_category = Category.objects.create(title='shoes', slug='shoes')
        self.new_category.save()
        credentials={
        'username' : 'maciej',
        'password1' : 'jaroszewski123',
        'password2' : 'jaroszewski123'
    }
        self.form = UserCreationForm(credentials)
        self.user = self.form.save()
        self.new_vendor = Vendor.objects.create(name=self.user.username, created_by=self.user)
        self.pk =self.new_vendor.id
        self.new_vendor.save()
        self.vendor_1 = Vendor.objects.get(id=self.pk)
        self.new_product = Product(
            category = self.new_category,
            vendor = self.vendor_1,
            title = 'nike',
            slug = 'nike',
            description = 'red snickers',
            price = 100
        )
        self.new_product.save()



    def tearDown(self):
        self.driver.close()


    def test_frontpage_view_is_displayed(self):
        self.driver.get(self.live_server_url)
        mp = MainPage(self.driver)
        self.assertEquals(
            mp.newest_products.text,
            "NEWEST PRODUCTS"
        )
        self.assertEquals(
            mp.product_price.text,
            (str(self.new_product.price) + '.00')
        )

    def test_frontpage_view_button(self):
        self.driver.get(self.live_server_url)
        mp = MainPage(self.driver)
        self.wait.until(E.element_to_be_clickable(mp.button_frontpage)).click()
        product_url = self.live_server_url + reverse('product',args= (self.new_category.slug, self.new_product.slug))
        self.assertEquals(
            self.driver.current_url,
            product_url
        )
        
    def test_frontpage_category_link(self):
        self.driver.get(self.live_server_url)
        mp = MainPage(self.driver)
        self.wait.until(E.element_to_be_clickable(mp.category_item)).click()
        category_url = self.live_server_url + reverse('category', args=(self.new_category.slug, ))
        self.assertEquals(
            self.driver.current_url,
            category_url
        )'''

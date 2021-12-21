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
        self.credentials={
        'username' : 'maciej',
        'password1' : 'jaroszewski123',
        'password2' : 'jaroszewski123'
    }
        self.form = UserCreationForm(self.credentials)
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
        search_results_page = page.SearchPage(self.driver)
        assert search_results_page.is_results_found()

    def test_login_page(self):
        self.driver.get('%s%s' % (self.live_server_url, '/vendors/login/'))
        login_page = page.LoginPage(self.driver)
        login_page.execute_login(self.credentials['username'], self.credentials['password1'])
        assert login_page.is_login_works()

    def test_logout_page(self):
        self.driver.get('%s%s' % (self.live_server_url, '/vendors/login/'))
        logout_page = page.LogoutPage(self.driver)
        logout_page.execute_login(self.credentials['username'], self.credentials['password1'])
        logout_page.logout()
        assert logout_page.is_logout_works(self.driver.title)

    def test_vendor_admin_page(self):
        self.driver.get('%s%s' % (self.live_server_url, '/vendors/login/'))
        vendor_admin = page.VendorAdminPage(self.driver)
        vendor_admin.execute_login(self.credentials['username'], self.credentials['password1'])
        new_email = 'maciej@gmail.com'
        vendor_admin.edit_vendor_email(new_email)
        assert vendor_admin.is_edit_vendor_works(self.driver.title)
        vendor_admin.click_vendors_link()
        assert vendor_admin.is_new_email_in_vendors_list(new_email)

    def test_cart_page(self):
        self.driver.get(self.live_server_url)
        cart_page = page.CartPage(self.driver)
        assert cart_page.is_adding_to_cart_works()
        assert cart_page.is_increasing_number_of_items_in_cart_works()
        assert cart_page.is_decreasing_number_of_items_in_cart_works()
        assert cart_page.is_total_cost_works()
        assert cart_page.is_removing_item_from_cart_works()
        
    def test_stripe_payment(self):
        self.driver.get(self.live_server_url)
        cart_page = page.CartPage(self.driver)
        assert cart_page.is_stripe_payment_works()

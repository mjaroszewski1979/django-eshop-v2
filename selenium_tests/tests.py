from selenium import webdriver
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from product.models import Product, Category
from django.contrib.auth.forms import UserCreationForm
from vendor.models import Vendor


class UrbanTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('selenium_tests/chromedriver.exe')
        self.browser.set_window_size(1920, 1080)
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

    def test_frontpage_category_link(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_class_name('category-item').click()
        category_url = self.live_server_url + reverse('category', args=(self.new_category.slug, ))
        self.assertEquals(
            self.browser.current_url,
            category_url
        )

    def test_frontpage_contact_link(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_class_name('contact-item').click()
        contact_url = self.live_server_url + reverse('contact')
        self.assertEquals(
            self.browser.current_url,
            contact_url
        )

    def test_frontpage_cart_link(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_class_name('cart').click()
        cart_url = self.live_server_url + reverse('cart')
        self.assertEquals(
            self.browser.current_url,
            cart_url
        )

    def test_frontpage_become_vendor_link(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_class_name('become-vendor').click()
        become_vendor_url = self.live_server_url + reverse('become_vendor')
        self.assertEquals(
            self.browser.current_url,
            become_vendor_url
        )
      
    def test_frontpage_vendors_link(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_class_name('vendors').click()
        vendors_url = self.live_server_url + reverse('vendors')
        self.assertEquals(
            self.browser.current_url,
            vendors_url
        )

    def test_frontpage_search_button(self):
        self.browser.get(self.live_server_url)
        time.sleep(10)
        search_button = self.browser.find_element_by_class_name('button-search')
        search_box = self.browser.find_element_by_class_name('search-box')
        search_url = self.live_server_url + reverse('search') + '?query=red'
        search_box.send_keys('red')
        search_button.click()
        
        self.assertEquals(
            self.browser.current_url,
            search_url
        )

    def test_search_page(self):
        self.browser.get('%s%s' % (self.live_server_url, ('/products/search/' + '?query=red')))
        time.sleep(5)
        search_term = self.browser.find_element_by_class_name('search-term')
        self.assertEquals(
            search_term.text,
            'SEARCH TERM: RED'
        )

    def test_login_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/vendors/login/'))
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        login = self.browser.find_element_by_class_name('vendor-login')
        username.send_keys('maciej')
        password.send_keys('jaroszewski123')
        login.click()
        time.sleep(10)
        vendor_admin = self.browser.find_element_by_class_name('vendor-admin')
        self.assertEquals(
            vendor_admin.text,
            'VENDOR ADMIN |'
        )

    def test_become_vendor_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/vendors/become_vendor/'))
        username = self.browser.find_element_by_name('username')
        password1 = self.browser.find_element_by_name('password1')
        password2 = self.browser.find_element_by_name('password2')
        button = self.browser.find_element_by_class_name('become-vendor')
        username.send_keys('newuser')
        password1.send_keys('topsecret123')
        password2.send_keys('topsecret123')
        button.click()
        time.sleep(10)
        vendor_admin = self.browser.find_element_by_class_name('vendor-admin')
        self.assertEquals(
            vendor_admin.text,
            'VENDOR ADMIN |'
        )
        self.assertEquals(
            self.browser.title,
            'Welcome | URBAN STYLE'
        )

    def test_logout_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/vendors/login/'))
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        login = self.browser.find_element_by_class_name('vendor-login')
        username.send_keys('maciej')
        password.send_keys('jaroszewski123')
        login.click()
        time.sleep(5)
        self.assertEquals(
            self.browser.title,
            'Vendor admin | URBAN STYLE'
        )
        logout = self.browser.find_element_by_class_name('logout')
        logout.click()
        time.sleep(5)
        self.assertEquals(
            self.browser.title,
            'Welcome | URBAN STYLE'
        )

    def test_edit_vendor_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/vendors/login/'))
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        login = self.browser.find_element_by_class_name('vendor-login')
        username.send_keys('maciej')
        password.send_keys('jaroszewski123')
        login.click()
        time.sleep(5)
        edit = self.browser.find_element_by_class_name('edit-vendor')
        edit.click()
        self.assertEquals(
            self.browser.title,
            'Edit vendor | URBAN STYLE'
        )

    def test_edit_vendor_email(self):
        self.browser.get('%s%s' % (self.live_server_url, '/vendors/login/'))
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        login = self.browser.find_element_by_class_name('vendor-login')
        username.send_keys('maciej')
        password.send_keys('jaroszewski123')
        login.click()
        time.sleep(5)
        edit = self.browser.find_element_by_class_name('edit-vendor')
        edit.click()
        time.sleep(5)
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys('maciej@gmail.com')
        submit = self.browser.find_element_by_class_name('edit-save')
        submit.click()
        time.sleep(5)
        self.assertEquals(
            self.browser.title,
            'Vendor admin | URBAN STYLE'
        )

    def test_edit_vendor_email_vendors_list(self):
        self.browser.get('%s%s' % (self.live_server_url, '/vendors/login/'))
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        login = self.browser.find_element_by_class_name('vendor-login')
        username.send_keys('maciej')
        password.send_keys('jaroszewski123')
        login.click()
        time.sleep(5)
        edit = self.browser.find_element_by_class_name('edit-vendor')
        edit.click()
        time.sleep(5)
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys('maciej@gmail.com')
        submit = self.browser.find_element_by_class_name('edit-save')
        submit.click()
        time.sleep(5)
        self.browser.find_element_by_class_name('vendors').click()
        time.sleep(5)
        address_list = self.browser.find_elements_by_tag_name('address')
        address = address_list[-1]
        self.assertEquals(
            address.text,
            'MACIEJ@GMAIL.COM'
        )

    def test_adding_product_to_cart(self):
        self.browser.get(self.live_server_url)
        time.sleep(2)
        self.browser.find_element_by_class_name('button-frontpage').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('add-to-cart').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('cart').click()
        time.sleep(2)
        self.assertEquals(
            self.browser.title,
            'Cart | URBAN STYLE'
        )

    def test_adding_multiple_products_to_cart(self):
        self.browser.get(self.live_server_url)
        time.sleep(2)
        self.browser.find_element_by_class_name('button-frontpage').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('add-to-cart').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('cart').click()
        time.sleep(2)
        self.browser.find_element_by_link_text('+').click()
        cart_items = self.browser.find_element_by_class_name('cart-length')
        self.assertEquals(
            cart_items.text,
            '2'
        )

    def test_updating_number_of_products_in_cart(self):
        self.browser.get(self.live_server_url)
        time.sleep(2)
        self.browser.find_element_by_class_name('button-frontpage').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('add-to-cart').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('cart').click()
        time.sleep(2)
        self.browser.find_element_by_link_text('+').click()
        time.sleep(2)
        self.browser.find_element_by_link_text('-').click()
        cart_items = self.browser.find_element_by_class_name('cart-length')
        self.assertEquals(
            cart_items.text,
            '1'
        )

    def test_cart_total_cost(self):
        self.browser.get(self.live_server_url)
        time.sleep(2)
        self.browser.find_element_by_class_name('button-frontpage').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('add-to-cart').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('cart').click()
        time.sleep(2)
        self.browser.find_element_by_link_text('+').click()
        time.sleep(2)
        cart_total_cost = self.browser.find_element_by_class_name('total-cost')
        self.assertEquals(
            cart_total_cost.text,
            '$200.00'
        )

    def test_removing_product_from_cart(self):
        self.browser.get(self.live_server_url)
        time.sleep(2)
        self.browser.find_element_by_class_name('button-frontpage').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('add-to-cart').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('cart').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('delete').click()
        cart_text = self.browser.find_element_by_class_name('cart-empty')
        self.assertEquals(
            cart_text.text,
            "YOU DON'T HAVE ANY PRODUCTS IN YOUR CART!"
        )

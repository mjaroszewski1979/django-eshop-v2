from selenium import webdriver
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse



class TestUrbanStyle(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('interiorshop/chromedriver.exe')

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
        self.browser.get('http://127.0.0.1:8000/products/search/?query=red')
        search_term = self.browser.find_element_by_class_name('search-term')
        self.assertEquals(
            search_term.text,
            'SEARCH TERM: RED'
        )

    def test_login_page(self):
        self.browser.get('http://127.0.0.1:8000/vendors/login/')
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        login = self.browser.find_element_by_class_name('vendor-login')
        username.send_keys('tomek')
        password.send_keys('haslo123')
        login.click()
        time.sleep(10)
        vendor_admin = self.browser.find_element_by_class_name('vendor-admin')
        self.assertEquals(
            vendor_admin.text,
            'VENDOR ADMIN |'
        )

    def test_become_vendor_page(self):
        self.browser.get('http://127.0.0.1:8000/vendors/become_vendor/')
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
        self.browser.get('http://127.0.0.1:8000/vendors/login/')
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        login = self.browser.find_element_by_class_name('vendor-login')
        username.send_keys('tomek')
        password.send_keys('haslo123')
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

 









      

    
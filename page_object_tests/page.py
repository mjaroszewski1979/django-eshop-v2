from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
from selenium_tests.locators import CartPageLocators, LoginPageLocators, LogoutPageLocators, MainPageLocators, VendorAdmiPageLocators, CartPageLocators
from selenium_tests.locators import SearchPageLocators
import time


class BasePage(object):


    def __init__(self, driver):
        self.driver = driver

    def do_click(self, locator):
        W(self.driver, 10).until(EC.visibility_of_element_located(locator)).click()

    def do_send_keys(self, locator, text):
        W(self.driver, 10).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def get_element(self, locator):
        element = W(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element

    def get_element_text(self, locator):
        element = W(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element.text

    def execute_login(self, username, password):
        self.do_send_keys(LoginPageLocators.USERNAME, username)
        self.do_send_keys(LoginPageLocators.PASSWORD, password)
        self.do_click(LoginPageLocators.LOGIN_BUTTON)

    def edit_vendor_email(self, email):
        self.do_click(VendorAdmiPageLocators.EDIT_VENDOR)
        self.do_send_keys(VendorAdmiPageLocators.VENDOR_EMAIL, email)
        self.do_click(VendorAdmiPageLocators.EDIT_BUTTON)

    def click_vendors_link(self):
        self.do_click(MainPageLocators.VENDORS)

    def click_view_button(self):
        self.do_click(MainPageLocators.VIEW_BUTTON)

    def click_cart_link(self):
        self.do_click(CartPageLocators.CART)

    def click_add_to_cart_button(self):
        self.do_click(CartPageLocators.ADD_TO_CART)

 




class MainPage(BasePage):


    def is_title_matches(self):
        return "Welcome | URBAN STYLE" in self.driver.title

    def is_view_button_works(self, title):
        return title in self.driver.title

    def click_category_link(self):
        self.do_click(MainPageLocators.CATEGORY_ITEM)

    def is_category_link_works(self, url):
        return url == self.driver.current_url

    def click_contact_link(self):
        self.do_click(MainPageLocators.CONTACT_ITEM)

    def is_contact_link_works(self, url):
        return url == self.driver.current_url

    def click_become_vendor_link(self):
        self.do_click(MainPageLocators.BECOME_VENDOR)

    def is_become_vendor_link_works(self, url):
        return url == self.driver.current_url

    def is_vendors_link_works(self, url):
        return url == self.driver.current_url

    def execute_search(self):
        self.do_send_keys(MainPageLocators.SEARCH_BOX, 'red')
        self.do_click(MainPageLocators.SEARCH_BUTTON)


class SearchPage(BasePage):


    def is_results_found(self):
        search_term = self.get_element_text(SearchPageLocators.SEARCH_TERM)
        return 'SEARCH TERM: RED' in search_term

class LoginPage(BasePage):

    def is_login_works(self):
        vendor_admin = self.get_element_text(VendorAdmiPageLocators.VENDOR_ADMIN)
        return vendor_admin == 'VENDOR ADMIN |'

class LogoutPage(BasePage):

    def logout(self):
        self.do_click(LogoutPageLocators.LOGOUT)

    def is_logout_works(self, title):
        return 'Welcome | URBAN STYLE' == title

class VendorAdminPage(BasePage):

    def is_edit_vendor_works(self, title):
        return 'Vendor admin | URBAN STYLE' == title

    def is_new_email_in_vendors_list(self, new_email):
        vendors_emails = self.get_element(VendorAdmiPageLocators.VENDORS_EMAILS)
        return new_email == vendors_emails.get_attribute('innerHTML')

class CartPage(BasePage):

    def is_adding_to_cart_works(self):
        self.click_view_button()
        self.click_add_to_cart_button()
        self.click_cart_link()
        return 'Cart | URBAN STYLE' in self.driver.title

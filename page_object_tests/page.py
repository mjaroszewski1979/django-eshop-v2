from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
from selenium_tests.locators import LoginPageLocators, LogoutPageLocators, MainPageLocators, VendorAdmiPageLocators
from selenium_tests.locators import SearchPageLocators


class BasePage(object):


    def __init__(self, driver):
        self.driver = driver

    def do_click(self, locator):
        W(self.driver, 10).until(EC.visibility_of_element_located(locator)).click()

    def do_send_keys(self, locator, text):
        W(self.driver, 10).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def get_element_text(self, locator):
        element = W(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element.text

    def execute_login(self, username, password):
        self.do_send_keys(LoginPageLocators.USERNAME, username)
        self.do_send_keys(LoginPageLocators.PASSWORD, password)
        self.do_click(LoginPageLocators.LOGIN_BUTTON)



class MainPage(BasePage):


    def is_title_matches(self):
        return "Welcome | URBAN STYLE" in self.driver.title

    def click_view_button(self):
        self.do_click(MainPageLocators.VIEW_BUTTON)

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

    def click_vendors_link(self):
        self.do_click(MainPageLocators.VENDORS)

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

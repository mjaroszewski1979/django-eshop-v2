from selenium_tests.element import BasePageElement
from selenium_tests.locators import MainPageLocators
from selenium_tests.locators import SearchPageLocators

class SearchTextElement(BasePageElement):

    locator = 'button-search'


class BasePage(object):


    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):

    search_text_element = SearchTextElement()

    def is_title_matches(self):

        return "Welcome | URBAN STYLE" in self.driver.title

    def click_view_button(self):

        element = self.driver.find_element(*MainPageLocators.VIEW_BUTTON)
        element.click()

    def is_view_button_works(self, title):

        return title in self.driver.title

    def click_category_link(self):

        element = self.driver.find_element(*MainPageLocators.CATEGORY_ITEM)
        element.click()

    def is_category_link_works(self, url):

        return url == self.driver.current_url

    def click_contact_link(self):

        element = self.driver.find_element(*MainPageLocators.CONTACT_ITEM)
        element.click()

    def is_contact_link_works(self, url):

        return url == self.driver.current_url

    def click_become_vendor_link(self):

        element = self.driver.find_element(*MainPageLocators.BECOME_VENDOR)
        element.click()

    def is_become_vendor_link_works(self, url):

        return url == self.driver.current_url

    def click_vendors_link(self):

        element = self.driver.find_element(*MainPageLocators.VENDORS)
        element.click()

    def is_vendors_link_works(self, url):

        return url == self.driver.current_url

    def execute_search(self):
        search_box = self.driver.find_element(*MainPageLocators.SEARCH_BOX)
        search_button = self.driver.find_element(*MainPageLocators.SEARCH_BUTTON)
        search_box.send_keys('red')
        search_button.click()


class SearchResultsPage(BasePage):


    def is_results_found(self):
        search_term = self.driver.find_element(*SearchPageLocators.SEARCH_TERM)
        return 'SEARCH TERM: RED' in search_term.text







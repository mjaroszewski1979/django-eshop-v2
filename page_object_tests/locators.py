from selenium.webdriver.common.by import By

class MainPageLocators(object):
    

    VIEW_BUTTON = (By.CLASS_NAME, 'button-frontpage')
    CATEGORY_ITEM = (By.CLASS_NAME, 'category-item')
    CONTACT_ITEM = (By.CLASS_NAME, 'contact-item')
    BECOME_VENDOR = (By.CLASS_NAME, 'become-vendor')
    VENDORS = (By.CLASS_NAME, 'vendors')
    SEARCH_BUTTON = (By.CLASS_NAME, 'button-search')
    SEARCH_BOX = (By.CLASS_NAME, 'search-box')
    
class SearchPageLocators(object):

    SEARCH_TERM = (By.CLASS_NAME, 'search-term')


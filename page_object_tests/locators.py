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

class LoginPageLocators(object):

    USERNAME = (By.NAME, 'username')
    PASSWORD = (By.NAME, 'password')
    LOGIN_BUTTON = (By.CLASS_NAME, 'vendor-login')

class LogoutPageLocators(object):

    LOGOUT = (By.CLASS_NAME, 'logout')

class VendorAdmiPageLocators(object):

    VENDOR_ADMIN = (By.CLASS_NAME, 'vendor-admin')
    EDIT_VENDOR = (By.CLASS_NAME, 'edit-vendor')
    VENDOR_EMAIL = (By.NAME, 'email')
    EDIT_BUTTON = (By.CLASS_NAME, 'edit-save')
    VENDORS_EMAILS = (By.TAG_NAME, 'address')

class CartPageLocators(object):

    ADD_TO_CART = (By.CLASS_NAME, 'add-to-cart')
    CART = (By.CLASS_NAME, 'cart')
    PLUS = (By.LINK_TEXT, '+')
    MINUS = (By.LINK_TEXT, '-')
    CART_LENGTH = (By.CLASS_NAME, 'cart-length')
    TOTAL_COST = (By.CLASS_NAME, 'total-cost')
    DELETE = (By.CLASS_NAME, 'delete')
    EMPTY = (By.CLASS_NAME, 'cart-empty')
    FIRST_NAME = (By.NAME, 'first_name')
    LAST_NAME = (By.NAME, 'last_name')
    EMAIL = (By.NAME, 'email')
    PHONE = (By.NAME, 'phone')
    ADDRESS = (By.NAME, 'address')
    ZIPCODE = (By.NAME, 'zipcode')
    PLACE = (By.NAME, 'place')
    IFRAME = (By.TAG_NAME, 'iframe')
    CARDNUMBER = (By.NAME, 'cardnumber')
    EXP_DATE = (By.NAME, 'exp-date')
    CVC = (By.NAME, 'cvc')
    POSTAL = (By.NAME, 'postal')
    CHECKOUT_BUTTON = (By.ID, 'checkout-button')
    TITLE = (By.CLASS_NAME, 'title')

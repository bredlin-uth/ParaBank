from selenium.webdriver.common.by import By

from utils.Web_Utils import WebUtils

class Register(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        # self.driver = driver

    register_link = (By.LINK_TEXT, "Register")
    first_name = (By.ID, "customer.firstName")
    last_name = (By.ID, "customer.lastName")
    address = (By.ID, "customer.address.street")
    city = (By.ID, "customer.address.city")
    state = (By.ID, "customer.address.state")
    zip_code = (By.ID, "customer.address.zipCode")
    phone = (By.ID, "customer.phoneNumber")
    ssn = (By.ID, "customer.ssn")
    username = (By.ID, "customer.username")
    password = (By.ID, "customer.password")
    confirm = (By.ID, "repeatedPassword")
    register_button = (By.XPATH,"//input[@value='Register']")
    log_out = (By.LINK_TEXT, "Log Out")

    def register_info(self, fname, lname, address, city, state, zipcode, phone, ssn, uname, pwd, pwd1):
        self.click_on_element(self.register_link)
        self.enter_text_in_field(self.first_name, fname)
        self.enter_text_in_field(self.last_name, lname)
        self.enter_text_in_field(self.address, address)
        self.enter_text_in_field(self.city, city)
        self.enter_text_in_field(self.state, state)
        self.enter_text_in_field(self.zip_code, zipcode)
        self.enter_text_in_field(self.phone, phone)
        self.enter_text_in_field(self.ssn, ssn)
        self.enter_text_in_field(self.username, uname)
        self.enter_text_in_field(self.password, pwd)
        self.enter_text_in_field(self.confirm, pwd1)
        self.click_on_element(self.register_button)
        self.click_on_element(self.log_out)








import logging

import allure
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
    sign_up_text = (By.XPATH, "//h1[normalize-space()='Signing up is easy!']")

    def verify_the_register_page(self):
        """
        Verify the Register Page.
        Returns True if the page is visible, else False.
        """
        with allure.step("Navigate to the Register page"):
            status = self.is_element_visible(self.sign_up_text)
            if status:
                self.logger.info("Navigate to the Register page")
            else:
                # allure.attach(self.driver.get_screenshot_as_png(), name="Bill Pay", attachment_type=AttachmentType.PNG)
                self.logger.error("Unable to navigate to the Register page")
        return status
    def registering_to_the_application(self, fname, lname, address, city, state, zipcode, phone, ssn, uname, pwd, pwd1):
        """
        Fills in the user details and submits the registration form
        Returns first name and user name used during registration
        """
        self.click_on_element(self.register_link)
        self.verify_the_register_page()
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
        allure.attach(self.driver.get_screenshot_as_png(), name="Form Filled: Registration", attachment_type=allure.attachment_type.PNG)
        self.click_on_element(self.register_button)

        return fname, uname
















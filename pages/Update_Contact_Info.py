import time

import allure
import pytest
from selenium.webdriver.common.by import By
from utils.Web_Utils import WebUtils

class UpdateContactInfo(WebUtils):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    Update_Contact_Info_linktext = (By.LINK_TEXT, "Update Contact Info")
    update_profile_firstname = (By.ID,"customer.firstName")
    update_profile_lastname = (By.ID,"customer.lastName")
    update_profile_address_street = (By.ID,"customer.address.street")
    update_profile_address_city = (By.ID,"customer.address.city")
    update_profile_address_state = (By.ID,"customer.address.state")
    update_profile_address_zipcode = (By.ID,"customer.address.zipCode")
    update_profile_phonenumber = (By.ID,"customer.phoneNumber")
    update_profile_btn = (By.XPATH,"//input[@value='Update Profile']")
    Profile_Updated = (By.XPATH,"//h1[normalize-space()='Profile Updated']")
    update_profile_error_xpath = (By.XPATH, "//p[@class='error']")

    def Update_Contact_Info(self,fristname,lastname,streetaddress,cityaddress,stateaddress,zipcodeaddress,phonenumber):
        """Update the user detail"""
        with allure.step("Update Contact Info"):
            self.click_on_Update_Contact_Info()
            self.enter_fristname_update_profile(fristname)
            self.enter_lastname_update_profile(lastname)
            self.enter_address_street_update_profile(streetaddress)
            self.enter_address_city_update_profile(cityaddress)
            self.enter_address_state_update_profile(stateaddress)
            self.enter_address_zipcode_update_profile(zipcodeaddress)
            time.sleep(3)
            self.enter_phonenumber_update_profile(phonenumber)
            time.sleep(5)
            self.click_on_Update_profile_btn()
            self.verify_profile_is_updated()

    def click_on_Update_Contact_Info(self):
        with allure.step(str("click_on_Update_Contact_Info").replace("_", " ")):
            self.click_on_element(self.Update_Contact_Info_linktext)

    def enter_fristname_update_profile(self,fristname):
        with allure.step(str("enter_fristname_update_profile").replace("_", " ")):
            self.enter_text_in_field(self.update_profile_firstname,fristname)

    def enter_lastname_update_profile(self,lastname):
        with allure.step(str("enter_lastname_update_profile").replace("_", " ")):
            self.enter_text_in_field(self.update_profile_lastname,lastname)

    def enter_address_street_update_profile(self,streetaddress):
        with allure.step(str("enter_address_street_update_profile").replace("_", " ")):
            self.enter_text_in_field(self.update_profile_address_street,streetaddress)

    def enter_address_city_update_profile(self,cityaddress):
        with allure.step(str("enter_address_city_update_profile").replace("_", " ")):
            self.enter_text_in_field(self.update_profile_address_city,cityaddress)

    def enter_address_state_update_profile(self,stateaddress):
        with allure.step(str("enter_address_state_update_profile").replace("_", " ")):
            self.enter_text_in_field(self.update_profile_address_state,stateaddress)

    def enter_address_zipcode_update_profile(self,zipcodeaddress):
        with allure.step(str("enter_address_zipcode_update_profile").replace("_", " ")):
            self.enter_text_in_field(self.update_profile_address_zipcode,zipcodeaddress)

    def enter_phonenumber_update_profile(self,phonenumber):
        with allure.step(str("enter_phonenumber_update_profile").replace("_", " ")):
            self.enter_text_in_field(self.update_profile_phonenumber,phonenumber)

    def click_on_Update_profile_btn(self):
        with allure.step(str("click_on_Update_profile_btn").replace("_", " ")):
            self.click_on_element(self.update_profile_btn)

    def verify_profile_is_updated(self):
        """verifying the user detail are updated by using Profile Updated keyword is displaying"""
        with allure.step(str("verify_profile_is_updated").replace("_", " ")):
            if self.wait_until_element_is_visible(self.Profile_Updated):
                with allure.step(f"Profile Updated"):
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Profile Updated",attachment_type=allure.attachment_type.PNG)
            elif self.wait_until_element_is_visible(self.update_profile_error_xpath):
                error_text = self.get_text_from_element(self.update_profile_error_xpath)
                self.logger.error(f"{error_text}")
                with allure.step(f"ERROR: {error_text}"):
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{error_text}",attachment_type=allure.attachment_type.PNG)
                    pytest.fail(f"{error_text}")

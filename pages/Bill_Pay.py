import inspect
import time

import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By

from utils import Common_Utils
from utils.Web_Utils import WebUtils


class BillPay(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    bill_payment_service_txt = (By.XPATH, "//h1[contains(text(),'Bill Payment Service')]")
    payee_name_tb = (By.NAME, "payee.name")
    address_tb = (By.NAME, "payee.address.street")
    city_tb = (By.NAME, "payee.address.city")
    state_tb = (By.NAME, "payee.address.state")
    zipcode_tb = (By.NAME, "payee.address.zipCode")
    phone_tb = (By.NAME, "payee.phoneNumber")
    account_tb = (By.NAME, "payee.accountNumber")
    verify_account_tb = (By.NAME, "verifyAccount")
    amount_tb = (By.NAME, "amount")
    from_account_dd = (By.NAME, "fromAccountId")
    send_payment_btn = (By.XPATH, "//input[@value='Send Payment']")
    bill_payment_complete_txt = (By.XPATH, "//h1[contains(text(),'Bill Payment Complete')]")
    bill_payment_success_msg = (By.XPATH, "//h1[contains(text(),'Bill Payment Complete')]/following-sibling::p")
    payee_name_txt = (By.ID, "payeeName")
    amount_txt = (By.ID, "amount")
    from_account_id_txt = (By.ID, "fromAccountId")

    def verify_the_transfer_funds_page(self):
        """
        Verify the Transfer Funds Page.
        Returns True if the page is visible, else False.
        """
        with allure.step("Navigate to the Bill Pay page"):
            status = self.is_element_visible(self.bill_payment_service_txt)
            if status:
                self.logger.info("Navigate to the Bill Pay page")
            else:
                # allure.attach(self.driver.get_screenshot_as_png(), name="Bill Pay", attachment_type=AttachmentType.PNG)
                self.logger.error("Unable to navigate to the Bill Pay page")
        return status

    def __select_from_account__(self):
        """
        Select from_account from the dropdown
        Returns from_account
        """
        options = self.get_values_from_the_dropdown(self.from_account_dd)
        self.select_by_value(self.from_account_dd, options[0])
        return options[0]

    def pay_bill(self, name, address, city, state, zipcode, phone, account, amount):
        """
        Pay Bill
        Returns from_account
        """
        self.enter_text_in_field(self.payee_name_tb, name)
        self.enter_text_in_field(self.address_tb, address)
        self.enter_text_in_field(self.city_tb, city)
        self.enter_text_in_field(self.state_tb, state)
        self.enter_text_in_field(self.zipcode_tb, zipcode)
        self.enter_text_in_field(self.phone_tb, phone)
        self.enter_text_in_field(self.account_tb, account)
        self.enter_text_in_field(self.verify_account_tb, account)
        self.enter_text_in_field(self.amount_tb, amount)
        from_account = self.__select_from_account__()
        self.select_by_visible_text(self.from_account_dd, from_account)
        self.click_on_element(self.send_payment_btn)
        return from_account

    def verify_transfer_complete(self, name, amount, from_account):
        """
        Verify the Transfer is completed.
        Returns True if the verification is success, else False
        """
        with allure.step(inspect.currentframe().f_code.co_name):
            time.sleep(3)
            if self.is_element_visible(self.bill_payment_complete_txt):
                name_result = self.get_text_from_element(self.payee_name_txt)
                amount_result = self.get_text_from_element(self.amount_txt)
                from_account_result = self.get_text_from_element(self.from_account_id_txt)
                transferred_success = self.get_text_from_element(self.bill_payment_success_msg)
                with allure.step(transferred_success): pass
                if Common_Utils.compare_currency_with_number(amount_result, amount) and name_result == name and from_account_result == from_account:
                    return True
                else:
                    return False
            else:
                return False


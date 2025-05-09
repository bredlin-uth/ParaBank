import re

import allure
import pytest

from utils.Web_Utils import WebUtils
from selenium.webdriver.common.by import By

class FindTransactions(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.transaction_id_text = None
        self.transaction_amount_text = None

    find_transaction_linktext = (By.LINK_TEXT,"Find Transactions")
    find_transaction_by_id = (By.ID,"transactionId")
    find_transaction_by_id_btn = (By.ID,"findById")

    find_transaction_date_id = (By.ID,"transactionDate")
    find_transaction_date_id_btn = (By.ID,"findByDate")

    find_transaction_daterange_between_id = (By.ID,"fromDate")
    find_transaction_daterange_to_id = (By.ID,"toDate")
    find_transaction_daterange_id_btn = (By.ID,"findByDateRange")

    find_transaction_amount_id = (By.ID,"amount")
    find_transaction_amount_id_btn = (By.ID,"findByAmount")

    find_transaction_table_id = (By.ID,"transactionTable")

    find_transaction_error_xpath = (By.XPATH,"//p[@class='error']")

    funds_transfer =(By.XPATH,"//a[contains(text(),'Funds Transfer Sent') or contains(text(),'Funds Transfer Received')]")

    transaction_id_text_xpath = (By.XPATH,"//b[normalize-space()='Transaction ID:']/parent::td/following-sibling::td")
    transaction_amount_text_xpath = (By.XPATH,"//b[normalize-space()= 'Amount:']/parent::td/following-sibling::td")

    def find_transaction_in_multiple_ways(self,find_transaction_value,transaction_values):
        try:
            with allure.step(str(find_transaction_value).replace("_"," ")):
                find_transaction_dicts = {
                    "find_transaction_id":self.find_transaction_using_id,
                    "find_transaction_date": self.find_transaction_using_date,
                    "find_transaction_daterange": self.find_transaction_using_daterange,
                    "find_transaction_amount": self.find_transaction_using_amount
                }
                try:
                    self.click_on_find_transaction()

                    func = find_transaction_dicts.get(str(find_transaction_value).lower())

                    if func:
                        func(transaction_values)
                        self.verify_transaction_history_present()
                        return self.transaction_id_text , self.transaction_amount_text
                    else:
                        raise ValueError(f"Invalid transaction type: {find_transaction_value}")
                finally:
                    self.click_on_find_transaction()
        except Exception as e:
            raise e

    def click_on_find_transaction(self):
        with allure.step(str("click_on_find_transaction").replace("_", " ")):
            self.click_on_element(self.find_transaction_linktext)

    ############## find_transaction_id ################
    def enter_transaction_id(self,transaction_id):
        with allure.step(str("enter_transaction_id").replace("_", " ")):
            self.enter_text_in_field(self.find_transaction_by_id,transaction_id)

    def click_on_find_transaction_id_btn(self):
        with allure.step(str("click_on_find_transaction_id_btn").replace("_", " ")):
            self.click_on_element(self.find_transaction_by_id_btn)

    def find_transaction_using_id(self,transaction_id):
        self.enter_transaction_id(transaction_id)
        self.click_on_find_transaction_id_btn()

    ############## find_transaction_date ################
    def enter_transaction_date(self,transaction_date):
        with allure.step(str("enter_transaction_date").replace("_", " ")):
            self.enter_text_in_field(self.find_transaction_date_id,transaction_date)

    def click_on_find_transaction_date_btn(self):
        with allure.step(str("click_on_find_transaction_date_btn").replace("_", " ")):
            self.click_on_element(self.find_transaction_date_id_btn)

    def find_transaction_using_date(self,transaction_date):
        self.enter_transaction_date(transaction_date)
        self.click_on_find_transaction_date_btn()

    ############## find_transaction_daterange ################
    def enter_transaction_daterange_between(self,transaction_daterange_between):
        with allure.step(str("enter_transaction_daterange_between").replace("_", " ")):
            self.enter_text_in_field(self.find_transaction_daterange_between_id,transaction_daterange_between)

    def enter_transaction_daterange_to(self,transaction_daterange_to):
        with allure.step(str("enter_transaction_daterange_to").replace("_", " ")):
            self.enter_text_in_field(self.find_transaction_daterange_to_id,transaction_daterange_to)

    def click_on_find_transaction_daterange_btn(self):
        with allure.step(str("click_on_find_transaction_daterange_btn").replace("_", " ")):
            self.click_on_element(self.find_transaction_daterange_id_btn)

    def find_transaction_using_daterange(self,transaction_daterange_values):
        transaction_daterange_between, transaction_daterange_to = transaction_daterange_values
        self.enter_transaction_daterange_between(transaction_daterange_between)
        self.enter_transaction_daterange_to(transaction_daterange_to)
        self.click_on_find_transaction_daterange_btn()

    ############## find_transaction_amount ################
    def enter_transaction_amount(self,transaction_amount):
        with allure.step(str("enter_transaction_amount").replace("_", " ")):
            self.enter_text_in_field(self.find_transaction_amount_id,transaction_amount)

    def click_on_find_transaction_amount_btn(self):
        with allure.step(str("click_on_find_transaction_amount_btn").replace("_", " ")):
            self.click_on_element(self.find_transaction_amount_id_btn)

    def find_transaction_using_amount(self,transaction_amount):
        self.enter_transaction_amount(transaction_amount)
        self.click_on_find_transaction_amount_btn()

    ############## verify_transaction_history_present ################
    def verify_transaction_history_present(self):
        self.transaction_id_text = None
        self.transaction_amount_text = None
        with allure.step(str("verify_transaction_history_present").replace("_", " ")):
            if self.wait_until_element_is_visible(self.find_transaction_table_id):
                with allure.step(f"Transaction Table"):
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Transaction Table",attachment_type=allure.attachment_type.PNG)
                if self.wait_until_element_is_visible(self.funds_transfer):
                    self.click_on_element(self.funds_transfer)
                    with allure.step(f"Transaction ID and Amount"):
                        allure.attach(self.driver.get_screenshot_as_png(), name=f"Transaction ID and Amount",attachment_type=allure.attachment_type.PNG)
                    id_text = self.get_text_from_element(self.transaction_id_text_xpath)
                    self.transaction_id_text = re.sub(r'[^\d.]', '', id_text)
                    amount_text = self.get_text_from_element(self.transaction_amount_text_xpath)
                    self.transaction_amount_text = re.sub(r'[^\d.]', '', amount_text)
                    with allure.step(f"Transaction ID: {self.transaction_id_text}"):pass
                    with allure.step(f"Transaction Amount: {self.transaction_amount_text}"): pass
            elif self.wait_until_element_is_visible(self.find_transaction_error_xpath):
                error_text = self.get_text_from_element(self.find_transaction_error_xpath)
                self.logger.error(f"{error_text}")
                with allure.step(f"ERROR: {error_text}"):
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{error_text}",attachment_type=allure.attachment_type.PNG)
                    pytest.fail(f"{error_text}")
import re

import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By

from utils import Common_Utils
from utils.Web_Utils import WebUtils


class TransferFunds(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    transfer_funds_txt = (By.XPATH, "//h1[contains(text(),'Transfer Funds')]")
    account_empty_msg = (By.XPATH, "//p[@id ='amount.errors' and contains(text(),'The amount cannot be empty.')]")
    enter_valid_amount_msg = (By.XPATH, "//p[@id ='amount.errors' and contains(text(),'Please enter a valid amount.')]")
    amount_tb = (By.ID, "amount")
    from_account_dd = (By.ID, "fromAccountId")
    to_account_dd = (By.ID, "toAccountId")
    transfer_btn = (By.XPATH, "//input[@value='Transfer']")
    transfer_complete_txt = (By.XPATH, "//h1[contains(text(),'Transfer Complete!')]")
    transferred_success_msg = (By.XPATH, "//h1[contains(text(),'Transfer Complete!')]/following-sibling::p")
    amount_result_txt = (By.ID, "amountResult")
    from_account_id_result_txt = (By.ID, "fromAccountIdResult")
    to_account_id_result_txt = (By.ID, "toAccountIdResult")

    def verify_the_transfer_funds_page(self):
        with allure.step("Navigate to the Transfer Funds page"):
            status = self.is_element_visible(self.transfer_funds_txt)
            if status:
                allure.attach(self.driver.get_screenshot_as_png(), name="Transfer Funds", attachment_type=AttachmentType.PNG)
                self.logger.info("Navigate to the Transfer Funds page")
            else:
                allure.attach(self.driver.get_screenshot_as_png(), name="Transfer Funds",
                              attachment_type=AttachmentType.PNG)
                self.logger.error("Unable to navigate to the Transfer Funds page")
        return status
    def transfer_funds(self, amount, from_account, to_account):
        self.enter_text_in_field(self.amount_tb, amount)
        self.select_by_visible_text(self.from_account_dd, from_account)
        self.select_by_visible_text(self.to_account_dd, to_account)
        self.click_on_element(self.transfer_btn)

    def verify_transfer_complete(self, amount, from_account, to_account):
        if self.is_element_visible(self.transfer_complete_txt):
            result_amount = self.get_text_from_element(self.amount_result_txt)
            from_account_id_result = self.get_text_from_element(self.from_account_id_result_txt)
            to_account_id_result = self.get_text_from_element(self.to_account_id_result_txt)
            transferred_success = self.get_text_from_element(self.transferred_success_msg)
            allure.attach(transferred_success, name="Transfer Funds", attachment_type=allure.attachment_type.TEXT)
            if Common_Utils.compare_currency_with_number(result_amount, amount) and from_account_id_result == from_account and to_account_id_result == to_account:
                return True
            else:
                return False
        else:
            return False


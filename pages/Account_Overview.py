import inspect
import time

import allure
from selenium.webdriver.common.by import By

from utils import Common_Utils
from utils.Common_Utils import *
from utils.Web_Utils import WebUtils


class AccountOverview(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    account_details = (By.XPATH, "//h1[contains(text(),'Account Details')]")
    account_details_txt = (By.XPATH, "//div[@id='accountDetails']/descendant::tr")
    account_id_txt = (By.ID, "accountId")
    account_type_txt = (By.ID, "accountType")
    balance_txt = (By.ID, "balance")
    available_balance_txt = (By.ID, "availableBalance")
    transaction_detail_title = (By.XPATH, "//h1[contains(text(), 'Transaction Details')]")
    transaction_details = (By.XPATH, "//h1[contains(text(), 'Transaction Details')]/following-sibling::table")

    def account_lnk(self, account_number):
        return By.XPATH, f"//table[@id='accountTable']/descendant::a[text()='{account_number}']"

    def account_overview_balance_txt(self, account):
        return By.XPATH, f"//td/a[text()='{account}']/../following-sibling::td[1]"

    def account_overview_available_balance_txt(self, account):
        return By.XPATH, f"//td/a[text()='{account}']/../following-sibling::td[2]"

    def transaction_lnk(self, amount, transaction_type):
        amount = str(convert_to_float_2dp(amount))
        if transaction_type == "Credit":
            return By.XPATH, f"//td[text()='${amount}']/preceding-sibling::td/a[contains(text(), 'Received')]"
        elif transaction_type == "Debit":
            return By.XPATH, f"//td[text()='${amount}']/preceding-sibling::td/a[contains(text(), 'Sent')]"
        elif transaction_type == "Down Payment":
            return By.XPATH, f"//td[text()='${amount}']/preceding-sibling::td/a[contains(text(), 'Down Payment')]"

    def transaction_detail_status(self, details):
        return By.XPATH, f"//b[contains(text(), '{details}')]/../following-sibling::td"


    def verify_the_account_details(self, account_number, account_type, balance, available_balance):
        """
        Verify the Account Details.
        Returns True if the verification is success, else False
        """
        with allure.step(inspect.currentframe().f_code.co_name):
            time.sleep(3)
            status = self.is_element_visible(self.account_details)
            if status:
                self.logger.info("Navigate to the Account Details page")
                exp_account_number = self.get_text_from_element(self.account_id_txt)
                exp_account_type = self.get_text_from_element(self.account_type_txt)
                exp_balance = self.get_text_from_element(self.balance_txt)
                exp_available_balance = self.get_text_from_element(self.available_balance_txt)
                if exp_account_number == account_number and exp_account_type == account_type and Common_Utils.compare_currency_with_number(exp_balance, balance) and Common_Utils.compare_currency_with_number(exp_available_balance, available_balance):
                    return True
                else:
                    return False
            else:
                # allure.attach(self.driver.get_screenshot_as_png(), name="Bill Pay", attachment_type=AttachmentType.PNG)
                self.logger.error("Unable to navigate to the Account Details page")
                return False

    def verify_the_account_and_click_on_account_number(self, account):
        """
        Verify the account and Click on the account number.
        Returns True if the verification is success, else False
        """
        time.sleep(5)
        status = self.is_element_visible(self.account_lnk(account))
        if status:
            balance = self.get_text_from_element(self.account_overview_balance_txt(account))
            available_balance = self.get_text_from_element(self.account_overview_balance_txt(account))
            if balance == available_balance:
                self.click_on_element(self.account_lnk(account))
                return True
        else:
            return False

    def click_on_the_transaction(self, amount, transaction_type):
        """
        Click on the Transaction.
        """
        self.click_on_element(self.transaction_lnk(amount, transaction_type))

    def verify_the_transaction_details(self, transaction, transaction_type, amount):
        """
        Verify the Transaction Details.
        Returns True if the verification is success, else False
        """
        with allure.step(inspect.currentframe().f_code.co_name):
            status = self.is_element_visible(self.transaction_detail_title)
            if status:
                details = self.get_text_from_element(self.transaction_details)
                allure.attach(details, name=f'{transaction}', attachment_type=allure.attachment_type.TEXT)
                description = self.get_text_from_element(self.transaction_detail_status("Description"))
                exp_type = self.get_text_from_element(self.transaction_detail_status("Type"))
                exp_amount = self.get_text_from_element(self.transaction_detail_status("Amount"))
                if description.__contains__(transaction) and exp_type == transaction_type and Common_Utils.compare_currency_with_number(exp_amount, amount):
                    return True
                else:
                    return False

    def get_the_transaction_id(self):
        """
        Get the transaction ID.
        Returns transaction_id.
        """
        transaction_id = self.get_text_from_element(self.transaction_detail_status("Transaction ID"))
        return transaction_id

    def get_the_transaction_date(self):
        """
        Get the transaction date.
        Returns transaction_date.
        """
        transaction_date = self.get_text_from_element(self.transaction_detail_status("Date"))
        return transaction_date


import inspect
import logging
import time
import allure
from selenium.webdriver.common.by import By
from utils.Web_Utils import WebUtils

class OpenNewAccount(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        # self.driver = driver

    type_of_account_dd = (By.XPATH, "//select[@id='type']")
    from_account_dd = (By.XPATH, "//select[@id='fromAccountId']")
    button_open_newaccount = (By.XPATH, "//input[@value='Open New Account']")
    # results_account_creation = (By.XPATH, "//div[@id='openAccountResult']")
    new_account_id_after_opening_account = (By.XPATH, "//a[@id='newAccountId']")

    def open_account(self, type_of_account):
        """
        Opens a new account by selecting the given account type and submitting the form.
        Parameters:
             type_of_account (str): The type of account to open (Savings, Checking)
        """
        try:
            with allure.step(f"Open New {type_of_account.capitalize()} Account"):
                self.select_by_visible_text(self.type_of_account_dd, type_of_account)
                self.select_by_index(self.from_account_dd, 0)
                allure.attach(self.driver.get_screenshot_as_png(), name="New Account: Open New Account",attachment_type=allure.attachment_type.PNG)
                self.click_on_element(self.button_open_newaccount)
        except Exception as e:
            raise e

    def get_newly_created_account_number(self):
        new_account_number_generated = self.get_text_from_element(self.new_account_id_after_opening_account)
        return new_account_number_generated

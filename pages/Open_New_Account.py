import inspect
import time
import allure
from selenium.webdriver.common.by import By
from utils.Web_Utils import WebUtils

class OpenNewAccount(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        #self.driver = driver

    type_of_account_dd = (By.XPATH, "//select[@id='type']")
    from_account_dd = (By.XPATH, "//select[@id='fromAccountId']")
    button_open_newaccount = (By.XPATH, "//input[@value='Open New Account']")
    new_account_id_after_opening_account = (By.XPATH, "//a[@id='newAccountId']")

    def open_account(self, type_of_account):

        try:
            with allure.step(f"Open New {type_of_account.capitalize()} Account"):
                self.select_by_visible_text(self.type_of_account_dd, type_of_account)
                self.select_by_index(self.from_account_dd, 0)
                self.click_on_element(self.button_open_newaccount)
                new_account_number_generated = self.get_text_from_element(self.new_account_id_after_opening_account)
                return type_of_account, new_account_number_generated
        except Exception as e:
            raise e





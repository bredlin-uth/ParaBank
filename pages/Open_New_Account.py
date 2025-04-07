import inspect
import time
import allure
from selenium.webdriver.common.by import By
from utils.Web_Utils import WebUtils
class OpenNewAccount(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        #self.driver = driver

    drop_down = (By.XPATH, "//select[@id='type']")
    drop_down1 = (By.XPATH, "//select[@id='fromAccountId']")
    button_open_newaccount = (By.XPATH, "//input[@value='Open New Account']")
    results_account_creation = (By.XPATH, "//div[@id='openAccountResult']")

    def open_account(self, type_of_account):
        try:
            with allure.step(f"Open New {type_of_account.capitalize()} Account"):
                self.select_by_visible_text(self.drop_down, type_of_account)
                self.select_by_index(self.drop_down1, 0)
                self.click_on_element(self.button_open_newaccount)
                return type_of_account
        except Exception as e:
            raise e

    # def new_checking_account(self,type_of_account):
    #     try:
    #         with allure.step("Open New Checking Account"):
    #             self.select_by_visible_text(self.drop_down,type_of_account)
    #             self.select_by_index(self.drop_down1,0)
    #             self.click_on_element(self.button_open_newaccount)
    #     except Exception as e:
    #         raise e
    #
    # def new_savings_account(self,type_of_account):
    #     try:
    #         with allure.step("Open New Savings Account"):
    #             self.select_by_visible_text(self.drop_down,type_of_account)
    #             self.select_by_index(self.drop_down1,0)
    #             self.click_on_element(self.button_open_newaccount)
    #     except Exception as e:
    #         raise e




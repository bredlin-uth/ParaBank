import time
import allure
from selenium.webdriver.common.by import By
from utils.Web_Utils import WebUtils

class AccountServices(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        # self.driver = driver

    log_out_lnk = (By.LINK_TEXT, "Log Out")
    register_success_msg = (By.XPATH, "//div[@id='rightPanel']")
    register_username_msg = (By.XPATH, "//div[@id='rightPanel']/h1[@class='title']")
    login_success_msg = (By.XPATH, "//p[@class='smallText']")
    account_opened_success_msg = (By.XPATH, "//div[@id='openAccountResult']")
    def account_services(self, services):
        return By.XPATH, f"//a[contains(text(),'{services}')]"

    def navigate_to_the_account_services(self, services):
        self.click_on_element(self.account_services(services))

    def verify_account_is_registered(self, uname):
        """
        Checks if the account is successfully registered by verifying the success message and matching the displayed username with the expected one.
        Parameters:
            uname (str): The expected username after registration.
        Returns:
            True if registration is successful and username matches, otherwise False.
        """
        time.sleep(3)
        if self.is_element_visible(self.register_success_msg):
            status_of_register = self.get_text_from_element(self.register_success_msg)
            username_result = self.get_text_from_element(self.register_username_msg)
            with allure.step(f" Verify account is registered {status_of_register} "):
                allure.attach(status_of_register, name="Verify account is registered", attachment_type=allure.attachment_type.TEXT)
                if uname in username_result:
                    return True
                else:
                    return False
        return False

    def log_out_from_application(self):
        self.click_on_element(self.log_out_lnk)

    def verify_account_is_logged_in(self, fname):
        """
        Checks if the account is successfully logged in by verifying the welcome message contains the user's first name.
        Parameters:
            fname (str): The expected first name displayed after login.
        Returns:
            True if login is successful and name matches, otherwise False.
        """
        time.sleep(3)
        if self.is_element_visible(self.login_success_msg):
            status_of_login = self.get_text_from_element(self.login_success_msg)
            with allure.step(f" Verify the account is logged in {status_of_login} "):
                allure.attach(status_of_login, name="Verify account Log in", attachment_type=allure.attachment_type.TEXT)
                if fname in status_of_login:
                    return True
                else:
                    return False
        return False

    def verify_new_account_opening(self, type_of_account):
        """
        Verifies if a new account of the specified type is successfully opened by checking for the success message.
        Parameters:
            type_of_account (str): The type of account that was attempted to open.
        Returns:
            True if the success message is visible, otherwise False.
        """
        time.sleep(3)
        if self.is_element_visible(self.account_opened_success_msg):
            status_of_account_opening = self.get_text_from_element(self.account_opened_success_msg)
            with allure.step(f" Verify new {type_of_account} account is opened {status_of_account_opening} "):
                allure.attach(status_of_account_opening, name="Verify new account opening", attachment_type=allure.attachment_type.TEXT)
                return True
        return False

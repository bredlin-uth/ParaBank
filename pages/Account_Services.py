import allure
from selenium.webdriver.common.by import By
from utils.Web_Utils import WebUtils

class AccountServices(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        # self.driver = driver

    log_out = (By.LINK_TEXT, "Log Out")
    register_success_msg = (By.XPATH, "//div[@id='rightPanel']")
    register_username_msg = (By.XPATH, "//div[@id='rightPanel']/h1[@class='title']")
    login_success = (By.XPATH, "//p[@class='smallText']")
    account_opened_success = (By.XPATH, "//div[@id='openAccountResult']")
    # new_account_id_after_opening_account = (By.XPATH, "//a[@id='newAccountId']")

    def account_services(self, services):
        return By.XPATH, f"//a[contains(text(),'{services}')]"

    def navigate_to_the_account_services(self, services):
        self.click_on_element(self.account_services(services))

    def verify_account_is_registered(self, uname):
        if self.is_element_visible(self.register_success_msg):
            status_of_register = self.get_text_from_element(self.register_success_msg)
            username_result = self.get_text_from_element(self.register_username_msg)
            with allure.step(f" Verify account is registered {status_of_register} "):
                allure.attach(self.driver.get_screenshot_as_png(), name="REGISTRATION",attachment_type=allure.attachment_type.PNG)
                if uname in username_result:
                    return True
                else:
                    return False
        return False

    def log_out_from_application(self):
        self.click_on_element(self.log_out)

    def verify_account_is_logged_in(self, fname):
        if self.is_element_visible(self.login_success):
            status_of_login = self.get_text_from_element(self.login_success)
            with allure.step(f" Verify the account is logged in {status_of_login} "):
                allure.attach(self.driver.get_screenshot_as_png(), name="LOGIN",attachment_type=allure.attachment_type.PNG)
                if fname in status_of_login:
                    return True
                else:
                    return False
        return False

    def verify_new_account_opening(self,type_of_account):
        if self.is_element_visible(self.account_opened_success):
            status_of_account_opening = self.get_text_from_element(self.account_opened_success)
            with allure.step(f" Verify new {type_of_account} account is opened {status_of_account_opening} "):
                allure.attach(self.driver.get_screenshot_as_png(), name="NEW ACCOUNT OPENING",attachment_type=allure.attachment_type.PNG)
                return True
        return False
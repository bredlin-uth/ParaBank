import allure
from selenium.webdriver.common.by import By
from utils.Web_Utils import WebUtils

class Login(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        # self.driver = driver

    username = (By.XPATH, "//div[@class='login']/input[@name='username']")
    password = (By.XPATH, "//div[@class='login']/input[@name='password']")
    login_button = (By.XPATH, "//div[@class='login']/input[@value='Log In']")

    def login_to_the_application(self, user_name, password):
        """
        Enters login details and submits the login form.
        """
        self.enter_text_in_field(self.username, user_name)
        self.enter_text_in_field(self.password, password)
        allure.attach(self.driver.get_screenshot_as_png(), name="Entered Credentials: Login",attachment_type=allure.attachment_type.PNG)
        self.click_on_element(self.login_button)











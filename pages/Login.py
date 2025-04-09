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
        self.enter_text_in_field(self.username, user_name)
        self.enter_text_in_field(self.password, password)
        self.click_on_element(self.login_button)


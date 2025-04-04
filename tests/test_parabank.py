import allure
import pytest
from pages.Open_New_Account import OpenNewAccount
from pages.Register import Register
from pages.Login import Login
from utils.Common_Utils import generate_random_user_for_registration
@pytest.mark.usefixtures("setup_and_teardown", "screenshot_on_failure")
class Test_Para_Bank:
    def test_main(self):
        try:
            with allure.step("Register to the ParaBank application"):
                register_page = Register(self.driver)
                user_data = generate_random_user_for_registration()
                register_page.register_info(**user_data)

            with allure.step("Login to the ParaBank application"):
                login_page = Login(self.driver)
                login_data = {
                    'user_name': user_data['uname'],  # Use registered email
                    'password': user_data['pwd']      # Use registered password
                }
                login_page.login_info(**login_data)

            with allure.step("Open New Account in the ParaBank application"):
                    checking_account_details = OpenNewAccount(self.driver)
                    checking_account_details.new_checking_account(type_of_account="CHECKING")
                    checking_account_details.new_savings_account(type_of_account="SAVINGS")

        except Exception as e:
            raise e
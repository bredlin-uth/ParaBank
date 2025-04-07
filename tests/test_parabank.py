import time

import allure
import pytest
from pages.Account_Services import AccountServices
from pages.Open_New_Account import OpenNewAccount
from pages.Register import Register
from pages.Login import Login
from utils.Common_Utils import generate_random_user_for_registration
@pytest.mark.usefixtures("setup_and_teardown", "screenshot_on_failure")
class Test_Para_Bank:

    def test_main(self):
        with allure.step("Register to the ParaBank application"):
            register_page = Register(self.driver) # creating object for Registration
            user_data = generate_random_user_for_registration()
            register_page.registering_to_the_application(**user_data)
            time.sleep(3)
            account_services = AccountServices(self.driver) # creating object for Account Services
            assert account_services.verify_account_is_registered(uname=user_data['uname'])
            account_services.log_out_from_application()

        with allure.step("Login to the ParaBank application"):
            login_page = Login(self.driver)
            login_data = {
                'user_name': user_data['uname'],  # Use registered email
                'password': user_data['pwd']      # Use registered password
            }
            login_page.login_to_the_application(**login_data)
            time.sleep(3)
            assert account_services.verify_account_is_logged_in(fname=user_data['fname'])

        with allure.step("Open New Accounts (Checking and Savings) in the ParaBank application"):
            account_details = OpenNewAccount(self.driver) #creating object for opening account
            for account_type in ["CHECKING", "SAVINGS"]:
                account_services.navigate_to_the_account_services("Open New Account")
                account_details.open_account(type_of_account=account_type)
                time.sleep(5)
                assert account_services.verify_new_account_opening(type_of_account=account_type)

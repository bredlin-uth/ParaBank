import time
import allure
import pytest
from pages.Account_Services import AccountServices
from pages.Bill_Pay import BillPay
from pages.Open_New_Account import OpenNewAccount
from pages.Register import Register
from pages.Login import Login
from pages.Request_Loan import RequestLoan
from pages.Transfer_Funds import TransferFunds
from utils.Common_Utils import *

@pytest.mark.usefixtures("setup_and_teardown", "screenshot_on_failure")
class Test_Para_Bank:

    def test_main(self):
        with allure.step("Register to the ParaBank application"):
            register_page = Register(self.driver)
            user_data = generate_random_user_for_registration()
            assert register_page.verify_the_register_page()
            register_page.registering_to_the_application(**user_data)
            time.sleep(3)
            account_services = AccountServices(self.driver)
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
            account_details = OpenNewAccount(self.driver)
            for account_type in ["CHECKING", "SAVINGS"]:
                account_services.navigate_to_the_account_services("Open New Account")
                account_details.open_account(type_of_account=account_type)
                time.sleep(5)
                assert account_services.verify_new_account_opening(type_of_account=account_type)

        with allure.step("Accounts Overview"):
            account_services.navigate_to_the_account_services("Accounts Overview")
            

        with allure.step("Bill Pay"):
            amount = 2
            account_services.navigate_to_the_account_services("Bill Pay")
            bill_pay_page = BillPay(self.driver)
            payee_details = generate_random_details_for_pay_bill(amount)
            assert bill_pay_page.verify_the_transfer_funds_page()
            from_account = bill_pay_page.pay_bill(**payee_details)
            assert bill_pay_page.verify_transfer_complete(payee_details['name'], payee_details['amount'], from_account)

        with allure.step("Transfer Funds"):
            amount = 3
            account_services.navigate_to_the_account_services("Transfer Funds")
            transfer_funds_page = TransferFunds(self.driver)
            assert transfer_funds_page.verify_the_transfer_funds_page()
            from_and_to_account = transfer_funds_page.transfer_funds(amount)
            assert transfer_funds_page.verify_transfer_complete(amount, from_and_to_account['from_account'], from_and_to_account['to_account'])

        with allure.step("Request Loan"):
            loan_amount = 200
            down_payment = 50
            account_services.navigate_to_the_account_services("Request Loan")
            request_loan_page = RequestLoan(self.driver)
            assert request_loan_page.verify_the_request_loan_page()
            from_account = request_loan_page.request_loan(loan_amount, down_payment)
            assert request_loan_page.verify_loan_request_complete()
            account_number = request_loan_page.get_new_account_number()

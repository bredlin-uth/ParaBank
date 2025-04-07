import allure
import pytest

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
                register_page.register_info(**user_data)

            with allure.step("Login to the ParaBank application"):
                login_page = Login(self.driver)
                login_data = {
                    'user_name': user_data['uname'],  # Use registered email
                    'password': user_data['pwd']      # Use registered password
                }
                login_page.login_info(**login_data)

            # with allure.step("Bill Pay"):
            #     amount = 2
            #     bill_pay_page = BillPay(self.driver)
            #     payee_details = generate_random_details_for_pay_bill(amount)
            #     assert bill_pay_page.verify_the_transfer_funds_page()
            #     from_account = bill_pay_page.pay_bill(**payee_details)
            #     assert bill_pay_page.verify_transfer_complete(payee_details['name'], payee_details['amount'], from_account)

            # with allure.step("Transfer Funds"):
            #     amount = 3
            #     transfer_funds_page = TransferFunds(self.driver)
            #     assert transfer_funds_page.verify_the_transfer_funds_page()
            #     from_and_to_account = transfer_funds_page.transfer_funds(amount)
            #     assert transfer_funds_page.verify_transfer_complete(amount, from_and_to_account['from_account'], from_and_to_account['to_account'])

            # with allure.step("Request Loan"):
            #     loan_amount = 200
            #     down_payment = 50
            #     request_loan_page = RequestLoan(self.driver)
            #     assert request_loan_page.verify_the_request_loan_page()
            #     from_account = request_loan_page.request_loan(loan_amount, down_payment)
            #     assert request_loan_page.verify_loan_request_complete()
            #     account_number = request_loan_page.get_new_account_number()

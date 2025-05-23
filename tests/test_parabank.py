from datetime import datetime
import time

import allure
import pytest

from pages.Account_Overview import AccountOverview
from pages.Account_Services import AccountServices
from pages.Bill_Pay import BillPay
from pages.Open_New_Account import OpenNewAccount
from pages.Register import Register
from pages.Login import Login
from pages.Request_Loan import RequestLoan
from pages.Transfer_Funds import TransferFunds
from utils.Common_Utils import *

from pages.Find_Transactions import FindTransactions
from pages.Update_Contact_Info import UpdateContactInfo

@pytest.mark.usefixtures("setup_and_teardown")
class Test_Para_Bank:
    user_data = {}
    transaction_id = None
    transaction_amount = None

    def test_register(self):
        global user_data
        with allure.step("Register to the ParaBank application"):
            register_page = Register(self.driver)
            user_data = generate_random_user_for_registration()
            register_page.registering_to_the_application(**user_data)
            account_services_page = AccountServices(self.driver)
            assert account_services_page.verify_account_is_registered(uname=user_data['uname'])
            account_services_page.log_out_from_application()

    def test_login(self):
        with allure.step("Login to the ParaBank application"):
            login_page = Login(self.driver)
            login_data = {
                'user_name': user_data['uname'],
                'password': user_data['pwd']
            }
            login_page.login_to_the_application(**login_data)
            account_services_page = AccountServices(self.driver)
            assert account_services_page.verify_account_is_logged_in(fname=user_data['fname'])

    def test_open_new_account(self):
        with allure.step("Open New Accounts (Checking and Savings) in the ParaBank application"):
            account_details = OpenNewAccount(self.driver)
            account_overview_page = AccountOverview(self.driver)
            account_services_page = AccountServices(self.driver)
            for account_type in ["CHECKING", "SAVINGS"]:
                account_services_page.navigate_to_the_account_services("Open New Account")
                account_details.open_account(type_of_account=account_type)
                assert account_services_page.verify_new_account_opening(type_of_account=account_type)
                new_account_number = account_details.get_newly_created_account_number()
                account_services_page.navigate_to_the_account_services("Accounts Overview")
                assert account_overview_page.verify_the_account_and_click_on_account_number(new_account_number)
                account_overview_page.verify_the_account_details(new_account_number, account_type, 100, 100)

    def test_bill_pay(self):
        with allure.step("Bill Pay"):
            bill_pay_amount = 2
            account_services_page = AccountServices(self.driver)
            account_services_page.navigate_to_the_account_services("Bill Pay")
            bill_pay_page = BillPay(self.driver)
            payee_details = generate_random_details_for_pay_bill(bill_pay_amount)
            assert bill_pay_page.verify_the_transfer_funds_page()
            from_account = bill_pay_page.pay_bill(**payee_details)
            assert bill_pay_page.verify_transfer_complete(payee_details['name'], payee_details['amount'], from_account)

    def test_transfer_funds(self):
        with allure.step("Transfer Funds"):
            transfer_funds_amount = 3
            account_services_page = AccountServices(self.driver)
            account_services_page.navigate_to_the_account_services("Transfer Funds")
            transfer_funds_page = TransferFunds(self.driver)
            assert transfer_funds_page.verify_the_transfer_funds_page()
            from_and_to_account = transfer_funds_page.transfer_funds(transfer_funds_amount)
            assert transfer_funds_page.verify_transfer_complete(transfer_funds_amount, from_and_to_account['from_account'], from_and_to_account['to_account'])

            account_overview_page = AccountOverview(self.driver)
            account_services_page.navigate_to_the_account_services("Accounts Overview")
            assert account_overview_page.verify_the_account_and_click_on_account_number(from_and_to_account['from_account'])
            account_overview_page.click_on_the_transaction(transfer_funds_amount, "Debit")
            account_overview_page.verify_the_transaction_details("Funds Transfer Sent", "Debit", transfer_funds_amount)
            sent_transaction_id = account_overview_page.get_the_transaction_id()
            sent_transaction_date = account_overview_page.get_the_transaction_date()

            account_services_page.navigate_to_the_account_services("Accounts Overview")
            assert account_overview_page.verify_the_account_and_click_on_account_number(from_and_to_account['to_account'])
            account_overview_page.click_on_the_transaction(transfer_funds_amount, "Credit")
            account_overview_page.verify_the_transaction_details("Funds Transfer Received", "Credit", transfer_funds_amount)
            received_transaction_id = account_overview_page.get_the_transaction_id()
            received_transaction_date = account_overview_page.get_the_transaction_date()

    def test_request_loan(self):
        with allure.step("Request Loan"):
            loan_amount = 10
            down_payment = 2
            account_services_page = AccountServices(self.driver)
            account_services_page.navigate_to_the_account_services("Request Loan")
            request_loan_page = RequestLoan(self.driver)
            assert request_loan_page.verify_the_request_loan_page()
            from_account = request_loan_page.request_loan(loan_amount, down_payment)
            assert request_loan_page.verify_loan_request_complete()
            account_number = request_loan_page.get_new_account_number()

            request_loan_page.click_on_the_new_account()
            account_overview_page = AccountOverview(self.driver)
            account_overview_page.verify_the_account_details(account_number, "LOAN", loan_amount, loan_amount)

            account_services_page.navigate_to_the_account_services("Accounts Overview")
            assert account_overview_page.verify_the_account_and_click_on_account_number(from_account)
            account_overview_page.click_on_the_transaction(down_payment, "Down Payment")
            account_overview_page.verify_the_transaction_details("Down Payment for Loan", "Debit", down_payment)
            loan_transaction_id = account_overview_page.get_the_transaction_id()
            loan_transaction_date = account_overview_page.get_the_transaction_date()

    def test_find_transaction_date(self):
        global transaction_id, transaction_amount
        findtransactions = FindTransactions(self.driver)
        transaction_date = datetime.now().strftime("%m-%d-%Y")
        transaction_id_text, transaction_amount_text = findtransactions.find_transaction_in_multiple_ways(
            find_transaction_value="find_transaction_date", transaction_values=transaction_date)
        transaction_id = transaction_id_text
        transaction_amount = transaction_amount_text

    def test_find_transaction_id(self):
        global transaction_id, transaction_amount
        findtransactions = FindTransactions(self.driver)
        if transaction_id:
            findtransactions.find_transaction_in_multiple_ways(find_transaction_value="find_transaction_id",transaction_values=transaction_id)
        else:
            raise ValueError(f"Give the Transaction ID")

    def test_find_transaction_daterange(self):
        global transaction_id, transaction_amount
        findtransactions = FindTransactions(self.driver)
        transaction_date = datetime.now().strftime("%m-%d-%Y")
        transaction_daterange_2value_list = (transaction_date, transaction_date)
        findtransactions.find_transaction_in_multiple_ways(find_transaction_value="find_transaction_daterange",transaction_values=transaction_daterange_2value_list)

    def test_find_transaction_amount(self):
        global transaction_id, transaction_amount
        findtransactions = FindTransactions(self.driver)
        if transaction_amount:
            findtransactions.find_transaction_in_multiple_ways(find_transaction_value="find_transaction_amount", transaction_values=transaction_amount)
        else:
            raise ValueError(f"Give the Transaction Amount")

    def test_update_contact_info(self):
        update_user_data = generate_random_user_for_registration()
        updatecontactinfo = UpdateContactInfo(self.driver)
        fristname, lastname, streetaddress, cityaddress, stateaddress, zipcodeaddress, phonenumber = \
        update_user_data['fname'], update_user_data['lname'], update_user_data['address'], update_user_data['city'], \
        update_user_data['state'], update_user_data['zipcode'], update_user_data['phone']
        updatecontactinfo.Update_Contact_Info(fristname, lastname, streetaddress, cityaddress, stateaddress,zipcodeaddress, phonenumber)

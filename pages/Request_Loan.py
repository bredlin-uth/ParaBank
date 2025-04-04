import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By

from utils.Web_Utils import WebUtils


class RequestLoan(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    apply_for_a_loan_txt = (By.XPATH, "//h1[contains(text(),'Apply for a Loan')]")
    loan_amount_tb = (By.ID, "amount")
    down_payment_tb = (By.ID, "downPayment")
    from_account_id_dd = (By.ID, "fromAccountId")
    apply_now_btn = (By.XPATH, "//input[@value='Apply Now']")
    loan_request_processed_txt = (By.XPATH, "//h1[contains(text(),'Loan Request Processed')]")
    loan_request_approved_txt = (By.ID, "loanRequestApproved")
    loan_request_denied_txt = (By.ID, "loanRequestDenied")
    new_account_id_txt = (By.ID, "newAccountId")
    request_loan_error_txt = (By.ID, "requestLoanError")
    # loan_provider_name_txt = (By.ID, "loanProviderName")
    loan_provider_info_txt = (By.XPATH, "//td[@id='loanProviderName']/parent::tr")
    # response_date_txt = (By.ID, "responseDate")
    loan_date_info_txt = (By.XPATH, "//td[@id='responseDate']/parent::tr")
    # loan_status_txt = (By.ID, "loanStatus")
    loan_status_info_txt = (By.XPATH, "//td[@id='loanStatus']/parent::tr")
    new_account_info_txt = (By.XPATH, "//a[@id='newAccountId']/parent::p")

    def verify_the_request_loan_page(self):
        with allure.step("Navigate to the Request Loan page"):
            status = self.is_element_visible(self.apply_for_a_loan_txt)
            if status:
                allure.attach(self.driver.get_screenshot_as_png(), name="Request Loan", attachment_type=AttachmentType.PNG)
                self.logger.info("Navigate to the Request Loan page")
            else:
                allure.attach(self.driver.get_screenshot_as_png(), name="Request Loan",
                              attachment_type=AttachmentType.PNG)
                self.logger.error("Unable to navigate to the Request Loan page")
        return status

    def request_loan(self, amount, down_payment, from_account):
        self.enter_text_in_field(self.loan_amount_tb, amount)
        self.enter_text_in_field(self.down_payment_tb, down_payment)
        self.select_by_visible_text(self.from_account_id_dd, from_account)
        self.click_on_element(self.apply_now_btn)

    def verify_transfer_complete(self, amount, from_account, to_account):
        if self.is_element_visible(self.loan_request_processed_txt):
            provider_info = self.get_text_from_element(self.loan_provider_info_txt)
            date_info = self.get_text_from_element(self.loan_date_info_txt)
            status_info = self.get_text_from_element(self.loan_status_info_txt)
            transferred_success = self.get_text_from_element(self.loan_request_approved_txt)
            allure.attach(provider_info, name="Request Loan", attachment_type=allure.attachment_type.TEXT)
            allure.attach(date_info, name="Request Loan", attachment_type=allure.attachment_type.TEXT)
            allure.attach(status_info, name="Request Loan", attachment_type=allure.attachment_type.TEXT)
            allure.attach(transferred_success, name="Request Loan", attachment_type=allure.attachment_type.TEXT)
            return True
        else:
            return False

    def get_new_account_number(self):
        account_number = self.get_text_from_element(self.new_account_id_txt)
        account_info = self.get_text_from_element(self.new_account_info_txt)
        allure.attach(account_info, name="Request Loan", attachment_type=allure.attachment_type.TEXT)
        return account_number

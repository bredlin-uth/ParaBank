import pytest
from pages.Find_Transactions import FindTransactions
from datetime import datetime

@pytest.mark.usefixtures("setup_and_teardown", "screenshot_on_failure")
class Test_FindTransactions:
    transaction_id = None
    transaction_amount = None

    @pytest.fixture(autouse=True)
    def setup(self, request):
        """Setup method to initialize FindTransactions with the WebDriver from fixtures."""
        self.driver = request.getfixturevalue("setup_and_teardown")  # Correct way to retrieve fixture
        self.findtransactions = FindTransactions(self.driver)

    def test_find_transaction_date(self):
        global transaction_id, transaction_amount
        transaction_date = datetime.now().strftime("%m-%d-%Y")
        transaction_id_text, transaction_amount_text = self.findtransactions.find_transaction_in_multiple_ways(find_transaction_value="find_transaction_date", transaction_values = transaction_date)
        transaction_id = transaction_id_text
        transaction_amount = transaction_amount_text

    def test_find_transaction_id(self):
        global transaction_id, transaction_amount
        if transaction_id:
            self.findtransactions.find_transaction_in_multiple_ways(find_transaction_value="find_transaction_id", transaction_values = transaction_id)
        else:
            raise ValueError(f"Give the Transaction ID")

    def test_find_transaction_daterange(self):
        transaction_date = datetime.now().strftime("%m-%d-%Y")
        transaction_daterange_2value_list = (transaction_date,transaction_date)
        self.findtransactions.find_transaction_in_multiple_ways(find_transaction_value="find_transaction_daterange", transaction_values = transaction_daterange_2value_list)

    def test_find_transaction_amount(self):
        global transaction_id, transaction_amount
        if transaction_amount:
            self.findtransactions.find_transaction_in_multiple_ways(find_transaction_value="find_transaction_amount", transaction_values = transaction_amount)
        else:
            raise ValueError(f"Give the Transaction Amount")
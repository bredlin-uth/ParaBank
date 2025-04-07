import pytest
from pages.Update_Contact_Info import UpdateContactInfo

@pytest.mark.usefixtures("setup_and_teardown", "screenshot_on_failure")
class Test_UpdateContactInfo:
    transaction_id = None
    transaction_amount = None

    @pytest.fixture(autouse=True)
    def setup(self, request):
        """Setup method to initialize UpdateContactInfo with the WebDriver from fixtures."""
        self.driver = request.getfixturevalue("setup_and_teardown")  # Correct way to retrieve fixture
        self.updatecontactinfo = UpdateContactInfo(self.driver)

    def test_update_contact_info(self):
        fristname, lastname, streetaddress, cityaddress, stateaddress, zipcodeaddress, phonenumber = " ", " ", " "," ", " "," "," "
        self.updatecontactinfo.Update_Contact_Info(fristname, lastname, streetaddress, cityaddress, stateaddress, zipcodeaddress,phonenumber)
from utils.Web_Utils import WebUtils


class UpdateContactInfo(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

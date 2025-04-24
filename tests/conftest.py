import os
import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import InvalidArgumentException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService

# Custom pytest command-line option to specify the browser
# Usage: pytest --browser chrome/firefox/edge
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use for tests: chrome, firefox, edge")

@pytest.fixture(scope="class")
def setup_and_teardown(request):
    """
    Fixture to initialize and tear down the WebDriver instance.
    - Choosing the browser choice from command-line options.
    - Initializes the WebDriver based on the selected browser.
    - Maximizes the browser window and sets an implicit wait.
    - Opens the URL.
    - Yields control to the test.txt.
    - Closes the WebDriver after the test.txt execution.
    """
    browser = request.config.getoption("--browser").lower()
    driver = None

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise InvalidArgumentException(f"Invalid browser selection: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(15)
    base_url = 'https://parabank.parasoft.com/parabank/register.htm'
    driver.get(base_url)

    request.cls.driver = driver  # Assign driver instance to the test.txt class
    yield driver  # Provide the driver instance to the test.txt
    driver.quit()

@pytest.fixture()
def screenshot_on_failure(request):
    """
    Fixture to capture a screenshot if a test.txt fails.
    - Executes after the test.txt.
    - If the test.txt fails, captures a screenshot and attaches it to the Allure report.
    """
    yield
    if request.node.rep_call.failed:
        driver = request.cls.driver
        if driver:
            allure.attach(driver.get_screenshot_as_png(), name="failed_test", attachment_type=AttachmentType.PNG)

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to generate test.txt reports.
    - Captures the test.txt result (pass/fail/skip) and attaches it to the test.txt item.
    - Enables checking test.txt status within fixtures.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

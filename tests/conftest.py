import os
import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import InvalidArgumentException

# Custom pytest command-line option to specify the browser
# Usage: pytest --browser chrome/firefox/edge
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use for tests: chrome, firefox, edge")

@pytest.fixture()
def setup_and_teardown(request):
    """
    Fixture to initialize and tear down the WebDriver instance.
    - Choosing the browser choice from command-line options.
    - Initializes the WebDriver based on the selected browser.
    - Maximizes the browser window and sets an implicit wait.
    - Opens the URL.
    - Yields control to the test.
    - Closes the WebDriver after the test execution.
    """
    browser = request.config.getoption("--browser").lower()
    driver = None

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(options=options)
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(options=options)
    else:
        raise InvalidArgumentException(f"Invalid browser selection: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(15)
    base_url = None
    driver.get(base_url)

    request.cls.driver = driver  # Assign driver instance to the test class
    yield driver  # Provide the driver instance to the test
    driver.quit()

@pytest.fixture()
def screenshot_on_failure(request):
    """
    Fixture to capture a screenshot if a test fails.
    - Executes after the test.
    - If the test fails, captures a screenshot and attaches it to the Allure report.
    """
    yield
    if request.node.rep_call.failed:
        driver = request.cls.driver
        if driver:
            allure.attach(driver.get_screenshot_as_png(), name="failed_test", attachment_type=AttachmentType.PNG)

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to generate test reports.
    - Captures the test result (pass/fail/skip) and attaches it to the test item.
    - Enables checking test status within fixtures.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

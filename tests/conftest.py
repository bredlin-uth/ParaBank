import os
from builtins import print
from datetime import datetime

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
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to use for tests: chrome, firefox, edge")


@pytest.fixture(scope="class")
def setup_and_teardown(request):
    """
    Main fixture to initialize and tear down the WebDriver instance.
    """
    browser = request.config.getoption("--browser").lower()
    driver = None

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        # options.add_argument("--headless")  # Add for CI
        # options.add_argument(f"--user-data-dir=/tmp/chrome-{os.getpid()}")  # Unique directory
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        # options.add_argument("--headless")  # Add for CI
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")  # Add for CI
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise InvalidArgumentException(f"Invalid browser selection: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(15)
    base_url = 'https://parabank.parasoft.com/parabank/register.htm'
    driver.get(base_url)

    request.cls.driver = driver
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configure automatic HTML reporting"""
    if not hasattr(config, 'workerinput'):
        report_dir = "./html-report"
        os.makedirs(report_dir, exist_ok=True)
        if not config.option.htmlpath:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            config.option.htmlpath = f"{report_dir}/report_{now}.html"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Main hook for screenshot attachment"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = getattr(item.instance, 'driver', None)
        if driver:
            try:
                # Take screenshot once
                screenshot_png = driver.get_screenshot_as_png()
                screenshot_base64 = driver.get_screenshot_as_base64()

                # 1. Attach to Allure report
                allure.attach(screenshot_png, name="failed_test", attachment_type=AttachmentType.PNG)

                # 2. Prepare for pytest-html report
                pytest_html = item.config.pluginmanager.getplugin("html")
                extra = getattr(report, "extra", [])

                # Add embedded image to HTML report
                extra.append(pytest_html.extras.image(screenshot_base64, 'Failure Screenshot'))

                # # 3. Save to file in report directory
                # report_dir = os.path.dirname(item.config.option.htmlpath)
                # screenshots_dir = os.path.join(report_dir, "screenshots")
                # os.makedirs(screenshots_dir, exist_ok=True)
                # timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                # screenshot_name = f"{item.name}_{timestamp}.png"
                # file_path = os.path.join(screenshots_dir, screenshot_name)
                #
                # with open(file_path, 'wb') as f:
                #     f.write(screenshot_png)
                #
                # # 4. Add working relative path link
                # rel_path = os.path.relpath(file_path, report_dir)
                # extra.append(pytest_html.extras.html(
                #     f'<div><a href="{rel_path}" target="_blank">View Full Screenshot</a></div>'
                # ))
                # # Add file link to HTML report
                # extra.append(pytest_html.extras.url(rel_path, name='Screenshot File'))

                report.extra = extra

            except Exception as e:
                print(f"Failed to capture and attach screenshots: {e}")

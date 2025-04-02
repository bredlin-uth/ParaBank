import pytest


@pytest.mark.usefixtures("setup_and_teardown", "screenshot_on_failure")
class Test_Demo:
    def test_demo(self):
        pass
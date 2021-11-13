import sys

print(sys.path)

from yadc.browser import Browser


def test_browser_default():
    with Browser() as driver:
        assert any(
            (
                "Driving license number" in driver.page_source,
                "Queue-it" in driver.page_source,
            )
        )

from yadc.browser import Browser, TorBrowser
import pytest
import shutil


def executable_path(*tries):
    """Find path to executable, or throw."""
    path = None
    for ex in tries:
        path = shutil.which(ex)
        if path:
            break

    if not path:
        raise Exception(f"Unable to find path to {tries[0]}")

    return path


@pytest.fixture
def chrome():
    return executable_path("chrome", "chromium", "google-chrome-stable", "chrome.exe")


@pytest.fixture
def chromedriver():
    return executable_path("chromedriver", "chromedriver.exe")


@pytest.fixture
def tor():
    return executable_path("tor", "TOR/tor.exe")


def test_browser():
    with Browser() as driver:
        assert any(
            (
                "Driving license number" in driver.page_source,
                "Queue-it" in driver.page_source,
            )
        )


def test_paths_chrome_chromedriver(chrome, chromedriver):
    with Browser(chrome=chrome, chromedriver=chromedriver) as driver:
        assert any(
            (
                "Driving license number" in driver.page_source,
                "Queue-it" in driver.page_source,
            )
        )


def test_paths_tor_browser(chrome, chromedriver, tor):
    with TorBrowser(chrome=chrome, chromedriver=chromedriver, tor=tor) as driver:
        assert any(
            (
                "Driving license number" in driver.page_source,
                "Queue-it" in driver.page_source,
            )
        )

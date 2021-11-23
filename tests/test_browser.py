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
    return executable_path(
        "chrome",
        "chromium",
        "google-chrome-stable",
        "chrome.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    )


@pytest.fixture
def chromedriver():
    return executable_path("chromedriver", "chromedriver.exe")


@pytest.fixture
def tor():
    return executable_path("tor", "Tor/tor.exe")


def run_test_browser(b):
    with b as driver:
        assert any(
            (
                "Driving license number" in driver.page_source,
                "Queue-it" in driver.page_source,
                "used queue number" in driver.page_source.lower(),
            )
        )


def test_browser():
    run_test_browser(Browser())


def test_paths_chrome_chromedriver(chrome, chromedriver):
    run_test_browser(Browser(chrome=chrome, chromedriver=chromedriver))


def test_paths_tor_browser(chrome, chromedriver, tor):
    run_test_browser(TorBrowser(chrome=chrome, chromedriver=chromedriver, tor=tor))

import pytest
import shutil
from yadc.browser import Browser


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


@pytest.fixture
def browser(chrome, chromedriver):
    return Browser(chrome=chrome, chromedriver=chromedriver)

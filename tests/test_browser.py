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
        assert driver.page_source


def test_paths_chrome_chromedriver_graphical(chrome, chromedriver):
    run_test_browser(Browser(chrome=chrome, chromedriver=chromedriver))


def test_paths_tor_browser_graphical(chrome, chromedriver, tor):
    run_test_browser(TorBrowser(chrome=chrome, chromedriver=chromedriver, tor=tor))


def test_dump_errors(mocker, tmp_path):
    mocker.patch.object(Browser, "__enter__")
    b = Browser(errors_dir=tmp_path)
    msg = "Test exception message"
    with pytest.raises(Exception):
        with b:
            raise Exception(msg)
    with next(tmp_path.glob("*.txt")).open() as f:
        assert msg in f.read()

    assert len(list(tmp_path.glob("*.html"))) == 1

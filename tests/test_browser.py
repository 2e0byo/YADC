from pathlib import Path

import pytest
from selenium.webdriver.common.by import By
from yadc.browser import Browser, ControlBrowserException, TorBrowser, BrowserError


def run_test_browser(b):
    with b as driver:
        assert driver.page_source


@pytest.mark.graphical
def test_paths_chrome_chromedriver_graphical(chrome, chromedriver):
    run_test_browser(Browser(chrome=chrome, chromedriver=chromedriver))


@pytest.mark.graphical
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


@pytest.mark.graphical
def test_take_control(mocker, chrome, chromedriver):
    mocked_input = mocker.patch("yadc.browser.input")
    with pytest.raises(ControlBrowserException):
        b = Browser(chrome=chrome, chromedriver=chromedriver)
        with b as driver:
            b.control_browser()
    mocked_input.assert_called_once_with("Press enter to exit.")


def page(pg):
    return f"file://{Path(__file__).parent}/pages/{pg}"


@pytest.mark.graphical
def test_wait_fail(chrome, chromedriver):
    b = Browser(chrome=chrome, chromedriver=chromedriver)
    with b as driver:
        driver.get(page("wait-page.html"))
        with pytest.raises(BrowserError, match="Page failed to load"):
            driver.find_element(By.ID, "no-such-element")

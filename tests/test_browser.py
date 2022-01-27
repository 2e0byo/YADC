from yadc.browser import Browser, TorBrowser
import pytest
from helper import chrome, chromedriver, tor


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

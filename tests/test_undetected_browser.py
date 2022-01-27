import shutil

import pytest
from selenium.webdriver.common.by import By
from yadc.undetected_browser import (
    ManualBusterUndetectedBrowser,
    ManualBusterUndetectedTorBrowser,
    UndetectedBrowser,
    UndetectedTorBrowser,
)


def pingtest(driver):
    driver.get("https://www.google.com")
    assert "Google Search" in driver.page_source


def run_browser_test(browser):
    unique_url = (
        "chrome-extension://mpbjkejclgfgadiemmefgebjfooflfhl/src/options/index.html"
    )
    with browser as driver:
        driver.get(unique_url)
        assert "Buster" in driver.page_source
        pingtest(driver)


@pytest.mark.graphical
@pytest.mark.manual
def test_manual_buster_undetected_browser(tmp_path):
    br = ManualBusterUndetectedBrowser(
        buster=True, profile_dir=(tmp_path) / "blank-profile"
    )
    run_browser_test(br)


@pytest.mark.graphical
def test_automated_manual_buster_undetected_browser(tmp_path):
    shutil.copytree("tests/blank-profile", tmp_path / "blank-profile")
    br = ManualBusterUndetectedBrowser(
        buster=True, profile_dir=(tmp_path) / "blank-profile"
    )
    run_browser_test(br)


@pytest.mark.graphical
@pytest.mark.manual
def test_manual_buster_undetected_tor_browser(tmp_path):
    br = ManualBusterUndetectedTorBrowser(
        buster=True, profile_dir=(tmp_path) / "blank-profile"
    )
    run_browser_test(br)


@pytest.mark.graphical
def test_automated_manual_buster_undetected_tor_browser(tmp_path):
    shutil.copytree("tests/blank-profile", tmp_path / "blank-profile")
    br = ManualBusterUndetectedTorBrowser(
        buster=True, profile_dir=(tmp_path) / "blank-profile"
    )
    run_browser_test(br)


@pytest.mark.graphical
def test_undetected_browser(tmp_path):
    br = UndetectedBrowser()
    with br as driver:
        pingtest(driver)


@pytest.mark.graphical
def test_undetected_tor_browser(tmp_path):
    br = UndetectedTorBrowser()
    with br as driver:
        pingtest(driver)


@pytest.mark.graphical
def test_buster_undetected_browser(tmp_path, buster):
    br = UndetectedBrowser(buster=buster)
    with br as driver:
        pingtest(driver)


@pytest.mark.graphical
def test_buster_undetected_tor_browser(tmp_path, buster):
    br = UndetectedTorBrowser(buster=buster)
    with br as driver:
        pingtest(driver)

import shutil
from json import load
from pathlib import Path
from time import sleep
from functools import partial

import psutil
import pytest
from selenium.webdriver.common.by import By
from undetected_chromedriver import dprocess
from yadc.undetected_browser import (
    ManualBusterUndetectedBrowser,
    ManualBusterUndetectedTorBrowser,
    UndetectedBrowser,
    UndetectedTorBrowser,
)


def pingtest(driver):
    driver.get("https://www.google.com")
    assert "Google Search" in driver.page_source


def _run_browser_test(fn, browser):
    with browser as driver:
        pid = psutil.Process(dprocess.REGISTERED[-1])
        assert pid.status() in ("running", "sleeping")
        fn(driver)

    try:
        count = 0
        while pid.status() and count < 10:
            sleep(1)
    except Exception:
        pass

    with pytest.raises(psutil.NoSuchProcess):
        pid.status()


run_pingtest = partial(_run_browser_test, pingtest)


def bustertest(driver):
    unique_url = "chrome-extension://src/options/index.html"
    try:
        with Path(driver.user_data_dir, "Default/Preferences").open() as f:
            data = load(f)
        secret, props = [
            (k, v)
            for k, v in data["extensions"]["settings"].items()
            if "buster" in v["path"]
        ][0]
        assert props["active_permissions"]
    except TypeError:
        secret = "mpbjkejclgfgadiemmefgebjfooflfhl"

    unique_url = f"chrome-extension://{secret}/src/options/index.html"
    driver.get(unique_url)
    assert "Buster" in driver.page_source
    pingtest(driver)


run_browser_test = partial(_run_browser_test, bustertest)


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
def test_manual_buster_undetected_tor_browser(tmp_path, tor):
    br = ManualBusterUndetectedTorBrowser(
        buster=True, profile_dir=(tmp_path) / "blank-profile", tor=tor
    )
    run_browser_test(br)


@pytest.mark.graphical
def test_automated_manual_buster_undetected_tor_browser(tmp_path, tor):
    shutil.copytree("tests/blank-profile", tmp_path / "blank-profile")
    br = ManualBusterUndetectedTorBrowser(
        buster=True, profile_dir=(tmp_path) / "blank-profile", tor=tor
    )
    run_browser_test(br)


@pytest.mark.graphical
def test_undetected_browser(tmp_path):
    br = UndetectedBrowser()
    run_pingtest(br)


@pytest.mark.graphical
def test_undetected_tor_browser(tmp_path, tor):
    br = UndetectedTorBrowser(tor=tor)
    run_pingtest(br)


@pytest.mark.graphical
def test_buster_undetected_browser(tmp_path):
    br = UndetectedBrowser(buster="tests/buster")
    run_browser_test(br)


@pytest.mark.graphical
def test_buster_undetected_tor_browser(tmp_path, tor):
    br = UndetectedTorBrowser(buster="tests/buster", tor=tor)
    run_browser_test(br)

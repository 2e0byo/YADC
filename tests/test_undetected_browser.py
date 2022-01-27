from selenium.webdriver.common.by import By
from yadc.undetected_browser import ManualBusterUndetectedBrowser


def test_manual_buster_undetected_browser(tmp_path):
    br = ManualBusterUndetectedBrowser(
        buster=True, profile_dir=(tmp_path) / "blank-profile"
    )
    unique_url = (
        "chrome-extension://mpbjkejclgfgadiemmefgebjfooflfhl/src/options/index.html"
    )
    with br as driver:
        driver.get(unique_url)
        assert "Buster" in driver.page_source

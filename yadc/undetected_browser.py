"""Browser and CaptchaChrome objects based around `undetected_chromedriver`."""
from pathlib import Path

from .browser import CaptchaChromeBase, Browser, TorBrowser, BrowserError
import undetected_chromedriver as us


class UndetectedCaptchaChrome(CaptchaChromeBase, uc.Chrome):
    """A CaptchaChrome based on `undetected_chromedriver`."""


class UndetectedBrowser(Browser):
    """A browser which lets `undetected_chromedriver` launch chrome for us."""

    def launch_chrome(self):
        pass

    def _connect(self, *args, chrome_options: uc.ChromeOptions = None):
        chrome_options = ChromeOptions or uc.ChromeOptions()
        if self._buster:
            chrome_options.add_argument(self.buster_arg)

        driver = UndetectedCaptchaChrome(options=chrome_options)

        driver.get(self._url)
        return driver


class UndetectedTorBrowser(UndetectedBrowser):
    @property
    def tor_arg(self):
        return f'--proxy-server="socks4://localhost:{self.tor_port}"'

    def _connect(self, *args, chrome_options: uc.ChromeOptions = None):
        chrome_options = ChromeOptions or uc.ChromeOptions()
        chrome_options.add_argument(self.tor_arg)
        return super()._connect(*args, chrome_options=chrome_options)


class ManualBusterMixin:
    BUSTER_URL = "https://chrome.google.com/webstore/detail/buster-captcha-solver-for/mpbjkejclgfgadiemmefgebjfooflfhl?hl=en"
    PROFILE_DIR = "blank-profile"

    def generate_profile(self):
        """Generate a profile and then install buster manually."""
        chrome_options = uc.ChromeOptions()
        chrome_options.user_data_dir = "blank-profile"
        driver = UndetectedCaptchaChrome(options=chrome_options)
        driver.get(self.BUSTER_URL)
        driver.find_element(By.XPATH, "//*[text()='I agree']").click()
        driver.find_element(
            By.CSS_SELECTOR, ".g-c-R.webstore-test-button-label"
        ).click()
        input("Accept installation and press enter: ")
        del driver

    def _connect(self, *args, chrome_options: uc.ChromeOptions = None):
        if self._buster:
            profile_dir = Path(self.PROFILE_DIR)
            if not profile_dir.is_dir():
                if profile_dir.exists():
                    raise BrowserError(
                        f"Profile dir {profile_dir} exists and is not a directory!"
                    )
                self.generate_profile()
            chrome_options.user_data_dir = self.PROFILE_DIR
            self._buster = None
        return super()._connext(*args, chrome_options=chrome_options)


class ManualBusterUndetectedBrowser(ManualBusterMixin, UndetectedBrowser):
    """A browser which installs buster manually and then uses the same profile dir."""


class ManualBusterUndetectedTorBrowser(ManualBusterMixin, UndetectedTorBrowser):
    """A tor browser which installs buster manually and then uses the same profile dir."""

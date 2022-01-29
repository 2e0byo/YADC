"""Browser and CaptchaChrome objects based around `undetected_chromedriver`."""
import multiprocessing
from logging import getLogger
from pathlib import Path

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from .browser import Browser, BrowserError, CaptchaChromeBase, TorBrowser

logger = getLogger(__name__)

# Monkeypatch undetected_chromedriver
# I'd love to know why we have to use shell=True to connect properly...


def _start_detached(executable, *args, writer: multiprocessing.Pipe = None):
    kwargs = {}
    if uc.dprocess.platform.system() == "Windows":
        kwargs.update(
            creationflags=uc.dprocess.DETACHED_PROCESS
            | uc.dprocess.CREATE_NEW_PROCESS_GROUP
        )
    elif uc.dprocess.sys.version_info < (3, 2):
        # assume posix
        kwargs.update(preexec_fn=uc.dprocess.os.setsid)
    else:  # Python 3.2+ and Unix
        kwargs.update(start_new_session=True)

    # run
    if not executable.startswith('"'):
        executable = f'"{executable}"'
    cmdline = " ".join([executable, *args])
    logger.debug(f"running chrome, cmdline is {cmdline}")
    PIPE = uc.dprocess.PIPE
    p = uc.dprocess.Popen(
        cmdline, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True, **kwargs
    )
    writer.send(p.pid)
    uc.sys.exit()


uc.dprocess._start_detached = _start_detached


class UndetectedCaptchaChrome(CaptchaChromeBase, uc.Chrome):
    """A CaptchaChrome based on `undetected_chromedriver`."""


class UndetectedBrowser(Browser):
    """A browser which lets `undetected_chromedriver` launch chrome for us."""

    def __init__(self, *args, chrome=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._chrome = f'"{chrome}"' if chrome else None

    def launch_chrome(self):
        pass

    def _connect(self, *args, chrome_options: uc.ChromeOptions = None):
        chrome_options = chrome_options or uc.ChromeOptions()
        if self._buster:
            chrome_options.add_argument(self.buster_arg)

        kwargs = {"options": chrome_options, "browser_executable_path": self._chrome}
        driver = UndetectedCaptchaChrome(**kwargs)
        self._proc = uc.dprocess.REGISTERED[-1]

        driver.get(self._url)
        return driver


class UndetectedTorBrowser(UndetectedBrowser, TorBrowser):
    # def start_tor(self):
    #     self._tor_port = 8897
    def launch_chrome(self):
        self.start_tor()

    @property
    def tor_arg(self):
        return f'--proxy-server="socks4://localhost:{self.tor_port}"'

    def _connect(self, *args, chrome_options: uc.ChromeOptions = None):
        chrome_options = chrome_options or uc.ChromeOptions()
        chrome_options.add_argument(self.tor_arg)
        return super()._connect(*args, chrome_options=chrome_options)


class ManualBusterMixin:
    BUSTER_URL = "https://chrome.google.com/webstore/detail/buster-captcha-solver-for/mpbjkejclgfgadiemmefgebjfooflfhl?hl=en"
    PROFILE_DIR = "blank-profile"

    def __init__(self, *args, profile_dir: Path = None, **kwargs):
        buster = kwargs.get("buster", None)
        if buster:
            del kwargs["buster"]
        super().__init__(*args, **kwargs)
        if buster:
            self._buster = buster
        self.profile_dir = profile_dir or self.PROFILE_DIR

    def generate_profile(self):
        """Generate a profile and then install buster manually."""
        chrome_options = uc.ChromeOptions()
        chrome_options.user_data_dir = self.profile_dir
        driver = UndetectedCaptchaChrome(options=chrome_options)
        driver.get(self.BUSTER_URL)
        driver.find_element(By.XPATH, "//*[text()='I agree']").click()
        driver.find_element(
            By.CSS_SELECTOR, ".g-c-R.webstore-test-button-label"
        ).click()
        input("Accept installation and press enter: ")
        driver.close()
        del driver

    def _connect(self, *args, chrome_options: uc.ChromeOptions = None):
        chrome_options = chrome_options or uc.ChromeOptions()
        if self._buster:
            profile_dir = Path(self.profile_dir)
            if not profile_dir.is_dir():
                if profile_dir.exists():
                    raise BrowserError(
                        f"Profile dir {profile_dir} exists and is not a directory!"
                    )
                self.generate_profile()
            chrome_options.user_data_dir = self.PROFILE_DIR
            self._buster = None
        return super()._connect(*args, chrome_options=chrome_options)


class ManualBusterUndetectedBrowser(ManualBusterMixin, UndetectedBrowser):
    """A browser which installs buster manually and then uses the same profile dir."""


class ManualBusterUndetectedTorBrowser(ManualBusterMixin, UndetectedTorBrowser):
    """A tor browser which installs buster manually and then uses the same profile dir."""

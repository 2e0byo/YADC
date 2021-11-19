import traceback as tb
from datetime import datetime
from logging import getLogger
from pathlib import Path
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory
from fake_useragent import UserAgent
from psutil import Process

import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.common.by import By

from .humanlike import randsleep


class BrowserError(Exception):
    pass


class CaptchaChrome(webdriver.Chrome):
    """A Chrome which will try to solve captchas for you."""

    INCAPSULA = "unsuccessful. Incapsula"
    BLOCKED = "Access denied"
    CAPTCHA_ATTEMPTS = 4
    instances = []

    def __init__(self, *args, **kwargs):
        i = max(self.instances) + 1 if self.instances else 1
        self.instances.append(i)
        name = f"CaptchaChrome-{i}"
        self._logger = getLogger(name)
        super().__init__(*args, **kwargs)

    def solve_captcha(self) -> bool:
        self.switch_to.default_content()
        iframe = self.find_element(value="main-iframe", bypass=False)
        self.switch_to.frame(iframe)
        iframe = self.find_element(
            By.CSS_SELECTOR,
            "iframe[name*='a-'][src*='https://www.google.com/recaptcha/api2/anchor?']",
            bypass=False,
        )
        self.switch_to.frame(iframe)
        randsleep(0.2)
        self.find_element(
            By.XPATH, "//span[@id='recaptcha-anchor']", bypass=False
        ).click()
        self.switch_to.default_content()
        randsleep(0.2)
        iframe = self.find_element(value="main-iframe", bypass=False)
        self.switch_to.frame(iframe)
        if "Why am I seeing this page" in self.page_source:
            self._logger.info("Completing catpcha 1")
            randsleep(0.2)

            iframe = self.find_element(
                By.CSS_SELECTOR,
                "iframe[title*='recaptcha challenge'][src*='https://www.google.com/recaptcha/api2/bframe?']",
                bypass=False,
            )
            self.switch_to.frame(iframe)
            randsleep(0.2)

            for _ in range(self.CAPTCHA_ATTEMPTS):
                self._logger.info("Completing catpcha")
                # let buster do it for us:
                self.find_elements(By.CLASS_NAME, "help-button-holder")[0].click()
                randsleep(5)
                if "Multiple correct solutions required" not in self.page_source:
                    break

            self.switch_to.default_content()
            randsleep(0.5)

        return "Why am I seeing this page" in self.page_source

    def bypass(self):
        """Try to bypass security."""

        solved = False
        if self.BLOCKED in self.page_source:
            self._logger.error("Blocked")
            raise BrowserError("Blocked")

        elif self.INCAPSULA in self.page_source:
            self._logger.info("Trying to solve captcha.")

            for _ in range(2):

                if (
                    self.INCAPSULA in self.page_source
                    and "iframe" not in self.page_source
                ):
                    randsleep(5)
                    self.refresh()
                else:
                    solved = True

                if self.INCAPSULA in self.page_source:
                    randsleep(2)
                    self.solve_captcha()
                else:
                    solved = True

                if self.INCAPSULA in self.page_source:
                    randsleep(150)
                else:
                    solved = True
        else:
            return

        if solved:
            self._logger.info("Solved Captcha!")
        else:
            self._logger.error("Unable to beat Captcha")
            raise BrowserError("Unable to beat Captcha")

    def find_element(self, by=None, value=None, bypass=True):
        if bypass:
            self.bypass()
        args = dict(by=by, value=value)
        return super().find_element(**{k: v for k, v in args.items() if v})


class Browser:
    """A browser driven by a driver over the debug interface.

    We start the browser *first* and navigate to the login page whilst the
    browser is 'clean', i.e. not controlled remotely.  This allows DVSA's
    profiling JS to run against a pretty clean browser.  We then block the
    profiling script, which seems to work, at least for a short while.
    (Otherwise we just get blocked.)"""

    URL = "https://driverpracticaltest.dvsa.gov.uk/login"
    instances = []

    def __init__(
        self,
        port: int = 8745,
        buster: Path = None,
        chrome: str = "google-chrome-stable",
        chromedriver: str = "chromedriver",
        url: str = None,
        errors_dir: Path = None,
        dump_on_error: bool = True,
    ):
        """Setup the Browser.

        Args:

            port (int): the port to use for remote management.  (Default: 8745)

            buster (Path): path to the unzipped buster extension.  If you don't
                           provide this, captchas will be unsolveable.

            chrome (str): path to the Chrome executable on your system.

            chromedrive_path(str): path to the chromedriver executable on your system.

            url (str): the url to point the browser to, if not the default DVSA one.

            errors_dir (Path): where to save errors.

            dump_on_error (bool): whether to save error dumps for debugging.
                                  (Default: True)
        """
        self._installed = False
        self._port = port
        if buster and not buster.is_dir():
            raise BrowserError("Please unzip buster and pass the dir.")
        self._buster = buster
        self._profile_dir = None
        self._chrome = chrome
        i = max(self.instances) + 1 if self.instances else 1
        self.instances.append(i)
        self.name = f"Browser-{i}"
        self._logger = getLogger(self.name)
        self._proc = None
        self._chromedriver = chromedriver
        self._url = url or self.URL
        self._errors_dir = errors_dir or Path(f"./errors/{self.name}")
        self.dump_on_error = dump_on_error

    @property
    def buster_arg(self) -> str:
        if self._buster:
            return f"--load-extension={self._buster}"
        else:
            return ""

    @property
    def profile_arg(self) -> str:
        if not self._profile_dir:
            self._profile_dir = TemporaryDirectory()
        return f"--user-data-dir={self._profile_dir.name}"

    @property
    def port_arg(self) -> str:
        return f"--remote-debugging-port={self._port}"

    def kill(self, proc, name):
        self._logger.info(f"Killing {name}")
        if not proc:
            return

        sysproc = Process(proc.pid)
        for child in sysproc.children(recursive=True):
            child.terminate()

        for child in sysproc.children(recursive=True):
            child.kill()

        proc.terminate()
        proc.wait(2)
        if proc.poll() is None:
            self._logger.info("Failed to die: killing with SIGKILL")
            proc.kill()
            proc.wait(2)
            if proc.poll() is None:
                raise BrowserError("Process failed to die")

    def launch_chrome(self, extra_args=None):
        self._logger.info("Starting chrome")
        ua = UserAgent().random
        self._logger.info(f"This time we are {ua}")
        cmd = [
            self._chrome,
            self.port_arg,
            self.profile_arg,
            self.buster_arg,
            "--no-first-run",
            "--blink-settings=imagesEnabled=false",
            f'--user-agent="{ua}"',
            self._url,
        ]
        if extra_args:
            cmd = cmd[:1] + extra_args + cmd[1:]
        # needed at present to prevent failure
        # chrome_options.experimental_options.pop("excludeSwitches")

        # Needed to launch in the right env with a new config
        # TODO: figure out what's actually happening here and fix this.
        self._proc = Popen(" ".join(cmd), shell=True)

    def __enter__(self) -> webdriver.Chrome:
        self.launch_chrome()

        self._logger.info("Waiting 10s for page to load and js to run.")
        randsleep(10)
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_experimental_option(
            "debuggerAddress", f"localhost:{self._port}"
        )

        driver = CaptchaChrome(
            executable_path=self._chromedriver,
            options=chrome_options,
        )

        driver.execute_cdp_cmd(
            "Network.setBlockedURLs",
            {
                "urls": [
                    "https://driverpracticaltest.dvsa.gov.uk/nions-to-vnse-the-Bewarfish-so-like-here-hoa-Mon"
                ]
            },
        )
        driver.execute_cdp_cmd("Network.enable", {})
        driver.refresh()
        self._driver = driver
        return driver

    def _dump(self, *err):
        self._errors_dir.mkdir(parents=True, exist_ok=True)
        outf = self._errors_dir / f"error-{datetime.now()}.txt"
        with outf.open("w") as f:
            f.write("".join(tb.format_exception(*err)))
            f.write("\n")
            f.write("Whilst visiting:")
            f.write(self._driver.current_url)
        with outf.with_suffix(".html").open("w") as f:
            f.write(self._driver.page_source)
        self._driver.save_screenshot(str(outf.with_suffix(".png")))
        self._logger.info(f"Saved error dump in {outf}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val and self.dump_on_error:
            try:
                self._dump(exc_type, exc_val, exc_tb)
            except Exception as e:
                tb.print_exc()

        self.kill(self._proc, "Chrome")
        self._profile_dir.cleanup()
        return False if exc_val else None


class TorBrowser(Browser):
    """A browser tunneled by TOR.

    We start the `tor` daemon ourselves so as to have a random IP. This will
    *only* work if you can run `tor` as your user. This will require removing
    the `User` option in the default `torrc`.

    The exit handler here kills the tor process, so we get a new ip for next
    time. This seems to reduce (although not eliminate?) getting profile
    blocked.
    """

    PORT = "8897"

    def start_tor(self):
        self._logger.info("Starting Tor")
        cmd = ["tor", "--SocksPort", self.PORT]
        proc = Popen(cmd, stdout=PIPE, encoding="utf8")
        self._tor_proc = proc
        self._logger.info("Started Tor")

    def launch_chrome(self):
        self.start_tor()
        tor_args = [
            f'--proxy-server="socks4://localhost:{self.PORT}"',
            # disable prefetch, as for some reason it's not proxied (?!)
            "--dns-prefetch-disable"
            # apparently this should be more resilient than merely disabling prefetch
            # but it doesn't seem to work
            # '--host-resolver-rules="MAP * ~NOTFOUND , EXCLUDE myproxy"',
        ]
        super().launch_chrome(extra_args=tor_args)

    def __exit__(self, *args):
        ret = super().__exit__(*args)
        self.kill(self._tor_proc, "Tor")
        return ret

import datetime as dt
import warnings
from collections import deque
from datetime import datetime
from logging import getLogger
from time import monotonic, sleep
from typing import Callable

from pydantic import BaseModel
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from .browser import Browser, BrowserError
from .humanlike import randsleep
from .utils import solve_captcha


class Test(BaseModel):
    """A driving test."""

    date: datetime
    centre: str


class Centre(BaseModel):
    """A centre and optional before date."""

    centre: str
    date: datetime = None


class Driver(BaseModel):
    "A driver seeking a driving test."
    licence_number: str
    booking_ref: str
    centres: list[Centre]
    not_before: datetime
    not_after: datetime
    disabled_dates: list[datetime] = None
    current_test: Test = None
    refresh_urls: dict = None


class ScraperError(Exception):
    pass


class BookingError(ScraperError):
    pass


class LoginError(Exception):
    pass


class Scraper:
    instances = []

    def __init__(
        self,
        browser: Browser,
        drivers: list[Driver],
        notify: Callable = None,
        reserve: bool = True,
        short_notice: bool = True,
    ):
        self._browser = browser
        self.notify = notify or print
        i = max(self.instances) + 1 if self.instances else 1
        self.instances.append(i)
        self.name = f"Browser-{i}"
        self._logger = getLogger(self.name)
        self.drivers = drivers
        for driver in self.drivers:
            driver.refresh_urls = {}
        self._logged_in = False
        self.reserve = reserve
        self.short_notice = short_notice

    @staticmethod
    def dvsa_disabled():
        return datetime.now().time() < dt.time(6) or datetime.now().time() > dt.time(
            23, 30
        )

    @staticmethod
    def input_text_box(el, text):
        for char in text:
            el.send_keys(char)
            randsleep(0.01)

    @staticmethod
    def parse_timestr(timestr: str) -> datetime:
        return datetime.strptime(timestr, "%A %d %B %Y %I:%M%p")

    def logged_in(self, browser) -> bool:
        return (
            self._logged_in
            and "queue" not in browser.current_url
            and "/login" not in browser.page_source
        )

    def login(self, browser: Chrome, driver: Driver):
        if self.logged_in(browser):
            return

        browser.bypass()
        if "queue" in browser.current_url:
            self._logger.info("Queuing...")
        while "queue" in browser.current_url:
            sleep(2)
        randsleep(3)
        browser.bypass()

        el = browser.find_element(value="driving-licence-number")
        el.click()
        randsleep(1)
        self.input_text_box(el, driver.licence_number)

        el = browser.find_element(value="application-reference-number")
        el.click()
        randsleep(1)
        self.input_text_box(el, driver.booking_ref)

        browser.find_element(value="booking-login").click()
        randsleep(3)

        if "loginError=true" in browser.current_url:
            raise LoginError("Unable to login.")
        self._logged_in = True

    def find_tests(self, browser: Chrome, driver: Driver):
        self.login(browser, driver)
        main = browser.find_element(value="main").get_attribute("innerHTML")
        if "has been cancelled" in main:
            raise ScraperError("Booking Cancelled.")
        elif "has now been exceeded" in main:
            raise ScraperError("Maximum rebookings exceeded.")

        contents_container = browser.find_elements(By.CLASS_NAME, "contents")
        if not contents_container:
            raise ScraperError("Failed to find contents container.")
        date = self.parse_timestr(
            contents_container[0]
            .find_element(By.XPATH, ".//dd")
            .get_attribute("innerHTML")
        )
        centre = (
            contents_container[1]
            .find_element(By.XPATH, ".//dd")
            .get_attribute("innerHTML")
        )
        driver.current_test = Test(date=date, centre=centre)
        for centre in driver.centres:
            randsleep(1.5)
            depth = self.find_next_available(browser, driver, centre)
            for _ in range(depth):
                browser.back()
                randsleep(0.5)

    def get_centre_url(self, browser, centre):
        browser.find_element(value="test-centre-change").click()
        randsleep(3)
        el = browser.find_element(value="test-centres-input")
        el.clear()
        self.input_text_box(el, centre)
        browser.find_element(value="test-centres-submit").click()
        randsleep(5)
        container = browser.find_element(By.CLASS_NAME, "test-centre-results")
        centre = container.find_element(By.XPATH, ".//a")
        return centre.get_attribute("href")

    def find_next_available(self, browser: Chrome, driver: Driver, centre: Centre):
        self._logger.info(f"Trying centre {centre.centre}")
        if centre.centre == driver.current_test.centre:
            back = 2
            browser.find_element(value="date-time-change").click()
            randsleep(1)
            browser.find_element(value="test-choice-earliest").click()
            randsleep(1)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            randsleep(1)
            browser.find_element(value="driving-licence-submit").click()
            randsleep(1)
        else:
            back = 3
            refresh_url = driver.refresh_urls.get(
                centre.centre, self.get_centre_url(browser, centre.centre)
            )
            browser.get(refresh_url)
            randsleep(1)

        page = browser.page_source
        with open("/tmp/test.html", "w") as f:
            f.write(page)
        if any(
            x in page
            for x in (
                "Oops",
                "in the queue",
                "Incapsula incident",
                "Enter details below",
            )
        ):
            browser.bypass()  # is this needed now we handle on getting?

        if "no tests available" in page:
            self._logger.info("No tests available.")
            return back

        day, el = self._scan_for_test(browser, driver, centre)
        if not day:
            self._logger.info("No tests in required range.")
            return back

        self.notify(f"Test found at {centre} on {day}")
        if self.reserve:
            slot = self._reserve_test(browser, day, el):
            if slot:
                self.logger.info(f"Reserved test: {slot}")
            else:
                self.logger.info("Failed to reserve test...")
                return back

        input("Press enter to continue")
        return back

    @staticmethod
    def correct_month_showing(browser: Chrome, day: datetime):
        el = browser.find_element(By.CLASS_NAME, "BookingCalendar-currentMonth")
        return day.strftime("%B") in el.get_attribute("innerHTML")

    def _reserve_test(self, browser: Chrome, day: datetime, el) -> bool:
        """Reserve a test.  **UNTESTED**"""
        warnings.warn(
            "Attempting to reserve test: code untested.  YMMV!", RuntimeWarning
        )

        # scroll to correct month
        attempts = 0
        while not self.correct_month_showing(browser, day):
            browser.find_element(By.CLASS_NAME, "BookingCalendar-nav--prev").click()
            attempts += 1
            if attempts > 12:
                raise BookingError("Failed to find correct month.")

        # click on date.
        el.click()
        # get container
        time_container = browser.find_element(By.ID, f"date-{day.strftime('%Y-%m-%d')}")
        label = time_container.find_element(By.XPATH, ".//label")
        # get time
        time_ms = int(label.get_attribute("for").replace("slot-", ""))
        time = datetime.fromtimestamp(hms_ms / 1000).time()
        test_slot = datetime.combine(day.date(), time)

        # check if short_notice
        short_notice = (
            label.get_attribute("for").get_attribute("data-short-notice") == "true"
        )
        # add error handling here if required.

        # click on label
        label.click()
        randsleep(0.1)

        # click on time container
        time_container.click()
        randsleep(0.1)

        # go for it
        driver.find_element_by_id("slot-chosen-submit").click()
        randsleep(0.1)

        # dismiss warning
        if short_notice:
            if self.short_notice:
                browser.find_element(
                    By.XPATH, "(//button[@id='slot-warning-continue'])[2]"
                ).click()
            else:
                self.logger.info("Skipping test as short notice.")
                return None
        else:
            browser.find_element_by_id("slot-warning-continue").click()

        randsleep(0.3)

        # this is wrapped in a loop in the original code.  I'm not sure what those multiple attempts are for.

        # we are the candidate
        browser.find_element(By.ID, "i-am-candidate").click()
        randsleep(0.1)

        # we make no manual attempt to solve the captcha here.  It might be
        # solved for us by the Browser().
        if "no longer available" in browser.page_source:
            self.logger.info("Missed it: someone else got there first...")
            return False

        return test_slot

    def _scan_for_test(self, browser: Chrome, driver: Driver, centre: Centre):
        cal = browser.find_element(By.CLASS_NAME, "BookingCalendar-datesBody")
        days = cal.find_elements(By.XPATH, ".//td")
        for day in days:
            if "--unavailable" in day.get_attribute("class"):
                continue
            a = day.find_element(By.XPATH, ".//a")
            date = datetime.strptime(a.get_attribute("data-date"), "%Y-%m-%d")

            # note that we cannot find multiple tests on the same day
            # this could be fixed, quite easily
            before_date = centre.date or driver.current_test.date
            if date.date() >= before_date.date():
                continue
            if driver.disabled_dates and date in driver.disabled_dates:
                continue
            elif date < driver.not_before:
                continue
            elif date > driver.not_after:
                continue
            return date, a

        return None, None

    def __call__(self):
        while True:
            self._logger.info("Starting search loop")

            if self.dvsa_disabled():
                self._logger.info("Website not currently available; sleeping.")

            while self.dvsa_disabled():
                randsleep(60)  # has spinner

            printed = False
            errs = deque([], maxlen=5)

            try:
                with self._browser as browser:
                    while True:
                        for driver in self.drivers:
                            self.find_tests(browser, driver)
                            randsleep(5 * 60)
            except Exception as e:
                errs.append(monotonic())
                self._logger.exception(e)
                randsleep(30)  # try not to be too predictable

            if len(errs) == 5 and errs[-1] - errs[0] < 10 * 60:
                msg = (
                    "Five errors within 10 minutes; "
                    "giving up so this IP doesn't get blacklisted."
                )
                self._logger.error(msg)  # make sure it's displayed, however we handle
                raise ScraperError(msg)

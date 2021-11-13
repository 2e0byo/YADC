from logging import getLogger

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from .humanlike import randsleep

logger = getLogger(__name__)

CAPTCHA_ATTEMPTS = 4


def solve_captcha(driver: Chrome) -> bool:
    driver.switch_to.default_content()
    iframe = driver.find_element(value="main-iframe")
    driver.switch_to.frame(iframe)
    iframe = driver.find_element(
        By.CSS_SELECTOR,
        "iframe[name*='a-'][src*='https://www.google.com/recaptcha/api2/anchor?']",
    )
    driver.switch_to.frame(iframe)
    randsleep(0.2)
    driver.find_element(By.XPATH, "//span[@id='recaptcha-anchor']").click()
    driver.switch_to.default_content()
    randsleep(0.2)
    iframe = driver.find_element(value="main-iframe")
    driver.switch_to.frame(iframe)
    if "Why am I seeing this page" in driver.page_source:
        logger.info("Completing catpcha 1")
        randsleep(0.2)

        iframe = driver.find_element(
            By.CSS_SELECTOR,
            "iframe[title*='recaptcha challenge'][src*='https://www.google.com/recaptcha/api2/bframe?']",
        )
        driver.switch_to.frame(iframe)
        randsleep(0.2)

        for _ in range(CAPTCHA_ATTEMPTS):
            logger.info("Completing catpcha")
            # let buster do it for us:
            driver.find_elements(By.CLASS_NAME, "help-button-holder")[0].click()
            randsleep(5)
            if "Multiple correct solutions required" not in driver.page_source:
                break

        driver.switch_to.default_content()
        randsleep(0.5)

    return "Why am I seeing this page" in driver.page_source

from time import sleep

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from app.config import MZ_LOGIN_USERNAME, MZ_LOGIN_PASSWORD, MZ_DOMAIN


def get_session_id(browser) -> str:
    if session_id := browser.get_cookie('PHPSESSID'):
        return session_id['value']
    return ''


def get_language(browser) -> str:
    if session_id := browser.get_cookie('MZLANG'):
        return session_id['value']
    return ''


def login(browser):
    browser.get(MZ_DOMAIN)
    sleep(5)

    browser.find_element_by_id("login_username").send_keys(MZ_LOGIN_USERNAME)
    browser.find_element_by_id("login_password").send_keys(MZ_LOGIN_PASSWORD)

    browser.find_element_by_css_selector(".floatLeft .buttonClassMiddle").click()
    element_visible = EC.visibility_of_element_located(locator=(By.ID, 'header-username'))
    WebDriverWait(browser, 20).until(element_visible)

import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome


class IsTherePlaces:
    def __init__(self, is_there: bool):
        self.is_there = is_there

    def __str__(self):
        if self.is_there:
            return 'СРОЧНО ПРОВЕРЬТЕ МЕСТА!!!!'
        else:
            return 'В настоящее время нет свободных мест для записи'

    def __eq__(self, other):
        if not isinstance(other, IsTherePlaces):
            return False
        else:
            return other.is_there == self.is_there


def check_places():
    options = Options()
    options.add_argument('--window-size=1920,1080')
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    driver = Chrome(chrome_options=options)

    try:
        login(driver)
        go_to_appointment_page(driver)
        choose_visa_type(driver)
        return is_there_places(driver)
    finally:
        driver.close()


def login(driver: WebDriver):
    driver.get('https://visa.vfsglobal.com/blr/ru/pol/login')
    time.sleep(5)
    driver.find_elements(by=By.XPATH, value='//input[@placeholder="jane.doe@email.com"]')[0]\
        .send_keys('arcimiendar@gmail.com')
    driver.find_elements(by=By.XPATH, value='//input[@formcontrolname="password"]')[0]\
        .send_keys('83Elilof*')
    driver.find_elements(by=By.XPATH, value='//form/button')[0]\
        .click()
    time.sleep(10)


def go_to_appointment_page(driver: WebDriver):
    els = driver.find_elements(by=By.XPATH, value='//*[contains(text(), "Записаться на прием")]')
    for el in els:
        try:
            el.click()
            time.sleep(5)
            return
        except Exception:
            pass


def choose_visa_type(driver: WebDriver):
    driver.find_elements(by=By.XPATH, value='//mat-select')[0]\
        .click()
    el = driver.find_elements(by=By.XPATH, value='//div[mat-option]')[0]
    el.send_keys()
    driver.find_elements(by=By.XPATH, value='//mat-option/span[contains(text(), "Center-Minsk")]')[0]\
        .click()
    time.sleep(5)

    driver.find_elements(by=By.XPATH, value='//mat-select')[1]\
        .click()
    driver.find_elements(by=By.XPATH, value='//mat-option')[0]\
        .click()
    time.sleep(5)

    driver.find_elements(by=By.XPATH, value='//mat-select')[2] \
        .click()
    driver.find_elements(by=By.XPATH, value='//mat-option')[1] \
        .click()
    time.sleep(5)


def is_there_places(driver: WebDriver):
    try:
        el = driver.find_elements(by=By.XPATH, value='//div[contains(@class, "alert")]')[0]
        is_there = el.text != 'В настоящее время нет свободных мест для записи'
    except Exception:
        is_there = False
    return IsTherePlaces(is_there)

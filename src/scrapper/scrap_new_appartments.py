import logging

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from sqlalchemy.orm import Session as DBSession
from selenium.webdriver import Chrome

from db.models import Appartment

logger = logging.getLogger(__name__)


def scrap_new_appartments(session: DBSession, url: str):
    appartments_all: list[Appartment] = get_appartments_from_main_page(session, url)

    new_appartments = []

    try:
        for appartment in appartments_all:
            if not session.query(Appartment).filter(Appartment.name == appartment.name).first():
                session.add(appartment)
                session.commit()
                new_appartments.append(appartment)
    finally:
        pass

    logger.info(f'scrapped {len(new_appartments)} new appartments')
    return new_appartments


def get_appartments_from_main_page(session: DBSession, url: str):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = Chrome(chrome_options=options)
    appartments = []
    with driver:
        driver.get(url)

        elems = driver.find_elements(
            value='//a[@data-cy="listing-item-link"]', by=By.XPATH
        )
        links = [elem.get_attribute('href') for elem in elems]
        for link in links:
            if session.query(Appartment).filter(Appartment.name == link).count():
                continue
            appartment = scrap_pecific_appartment(link, driver)
            if appartment:
                appartments.append(appartment)
    return appartments


def scrap_pecific_appartment(link: str, driver: WebDriver) -> None | Appartment:
    appartment = Appartment(name=link)
    driver.get(link)
    price_elements = driver.find_elements(value='//strong[@aria-label="Cena"]', by=By.XPATH)
    if not price_elements:
        return None

    text_parts = price_elements[0].text.split()
    appartment.price = int(''.join([part for part in text_parts if part.isdigit()]))

    czynsz_elements = driver.find_elements(by=By.XPATH, value='//div[@aria-label="Czynsz"]/div[2]')
    if czynsz_elements:
        parts = czynsz_elements[0].text.split()
        czynsz_str = ''.join([part for part in parts if part.isdigit()])
        if czynsz_str:
            czynsz = int(czynsz_str)
        else:
            czynsz = 0
    else:
        czynsz = 0
    appartment.czynsz = czynsz

    rooms_elements = driver.find_elements(by=By.XPATH, value='//div[@aria-label="Liczba pokoi"]/div[2]')
    if not rooms_elements:
        return None
    appartment.rooms = int(rooms_elements[0].text)
    return appartment

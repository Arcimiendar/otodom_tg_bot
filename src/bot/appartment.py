import time
import logging

from telegram.ext import ExtBot

from db import Session
from db.models import Appartment, User
from scrapper.scrap_new_appartments import scrap_new_appartments

logger = logging.getLogger(__name__)


def scrapper(bot: ExtBot, url: str):
    while True:
        try:
            logger.info('start scrapper iteration')
            session = Session()
            with session:
                new_appartments: list[Appartment] = scrap_new_appartments(session, url)
                if new_appartments:
                    users: list[User] = session.query(User).all()

                    for user in users:
                        for appartment in new_appartments:
                            bot.send_message(user.id, str(appartment))
        except Exception as e:
            logger.error('huston: %s' % e, exc_info=True)

        time.sleep(60)

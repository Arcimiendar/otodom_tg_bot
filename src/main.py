import logging
# import db
import os

from telegram.ext import Updater, Dispatcher, ExtBot

from bot.appartment import ScrapperManager
from bot.start import start_command


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_urls() -> list[str]:
    urls = []
    with open('/app/urls_to_scrap.txt') as f:
        while (line := f.readline()) != '':
            line = line.strip()
            logger.info(f'got line: {line}')
            if (line or '#')[0] != '#':
                urls.append(line)
    return urls


def main():
    updater = Updater(token=os.environ['BOT_TOKEN'], use_context=True)

    dp: Dispatcher = updater.dispatcher

    dp.add_handler(start_command)
    bot: ExtBot = dp.bot
    urls = parse_urls()

    manager = ScrapperManager(urls, bot)
    manager.start()

    updater.start_polling()
    manager.join()


if __name__ == '__main__':
    main()

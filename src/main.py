import logging
# import db
import os

from telegram.ext import Updater, Dispatcher, ExtBot
from threading import Thread

from bot.appartment import scrapper
from bot.start import start_command


logging.basicConfig(level=logging.INFO)


def main():
    updater = Updater(token=os.environ['BOT_TOKEN'], use_context=True)

    dp: Dispatcher = updater.dispatcher

    dp.add_handler(start_command)
    bot: ExtBot = dp.bot
    thread1 = Thread(target=scrapper, args=(
        bot,
        'https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/'
        'wroclaw?distanceRadius=0&page=1&limit=36&market=ALL&ownerTypeSingleSelect=ALL&'
        'roomsNumber=%5BONE%2CTWO%2CTHREE%5D&locations=%5Bcities_6-39%5D&'
        'sviewType=listing&by=LATEST&direction=DESC'
    ))
    thread2 = Thread(target=scrapper, args=(
        bot,
        'https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/poznan?roomsNumber=%5BONE%5D&by=LATEST&direction=DESC'
    ))
    thread1.start()
    thread2.start()

    updater.start_polling()
    thread1.join()
    thread2.join()


if __name__ == '__main__':
    main()

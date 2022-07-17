from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from db import Session
from db.models import User


def start(update: Update, _: CallbackContext):
    session = Session()
    with session:
        if session.query(User).filter(User.id == update.message.from_user.id).first() is None:
            user = User(id=update.message.from_user.id)
            session.add(user)
            session.commit()
    update.message.reply_text('ща квартиры полетят')


start_command = CommandHandler('start', start)

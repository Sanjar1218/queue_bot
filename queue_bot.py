# import context and update
from telegram.ext import CallbackContext
from telegram import Update

# start function
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Salom navbatchilik botiga xush kelibsiz")



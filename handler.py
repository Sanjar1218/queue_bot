# import updater and dispatcher
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# import functions
from queue_bot import start

# import from env
import os

TOKEN = os.environ.get("TOKEN")

# create updater and dispatcher
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# add handlers
dispatcher.add_handler(CommandHandler("start", start))

# start polling
updater.start_polling()

updater.idle()
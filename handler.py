# import updater and dispatcher
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# import functions
from queue_bot import (
    start,
    create_group,
    accept,
    accept_callback,
    create_queue,
    create_admin,
    is_done
)

# import from env
import os

TOKEN = os.environ.get("TOKEN")

# create updater and dispatcher
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# add handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("create_group", create_group))
dispatcher.add_handler(CallbackQueryHandler(accept, pattern='[0-9]+'))
dispatcher.add_handler(CallbackQueryHandler(accept_callback, pattern='[a-z]+'))
dispatcher.add_handler(CommandHandler("create_queue", create_queue))
dispatcher.add_handler(CommandHandler("create_admin", create_admin))
dispatcher.add_handler(CommandHandler("is_done", is_done))

# start polling
updater.start_polling()

updater.idle()
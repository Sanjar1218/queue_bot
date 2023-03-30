# import context and update
from telegram.ext import CallbackContext
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# import db
from db import Database

from datetime import date

# start function
def start(update: Update, context: CallbackContext):
    # save all user data
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    # create database object
    db = Database()

    # save user
    db.add_user(user_id, username, first_name, last_name)

    # send button create group
    button = KeyboardButton('Create group')
    button2 = KeyboardButton('Bugungi navbatchilar')
    markup = ReplyKeyboardMarkup([[button, button2]], resize_keyboard=True)

    update.message.reply_text("Salom navbatchilik botiga xush kelibsiz\nGrouppa yaratish uchun pastki tugmani bosing", reply_markup=markup)

# create group function
def create_group(update: Update, context: CallbackContext):
    # save user id
    user_id = update.message.from_user.id

    # create database object
    db = Database()

    # add group to database
    group_id = db.add_group(user_id)

    # send inline buttons that shows users name in the callback user_id
    buttons = []
    for i in db.user.all():
        # don't add user that is already in the group
        buttons.append([InlineKeyboardButton(i['first_name'], callback_data=f"{i['user_id']}_{group_id}")])

    markup = InlineKeyboardMarkup(buttons)

    # send message
    if buttons:
        update.message.reply_text("Guruh yaratildi\nSherigingizni tanlang!", reply_markup=markup)
    else:
        update.message.reply_text('Hech qanday user yoq iltimos kuting yangi user qo\'shilgancha')

# Accept callback function
def accept(update: Update, context: CallbackContext):
    # get callback data
    chosen_id = int(update.callback_query.data)

    # user id
    user_id = update.callback_query.from_user.id

    # create database object
    db = Database()

    # send message to chosen user with inline button accept or not
    buttons = [InlineKeyboardButton('Roziman✅', callback_data=f'accept_{user_id}'), InlineKeyboardButton('Noroziman❌', callback_data=f'notaccept_{user_id}')]
    markup = InlineKeyboardMarkup([buttons])

    # asnwer callback
    update.callback_query.answer('Xabaringiz jonatildi')
    # send message to chosen user
    context.bot.send_message(chosen_id, f"{db.get_user(user_id)['first_name']} sizni guruhga qo'shmoqchi\nQo'shishni roziman bo'lsangiz pastki tugmani bosing", reply_markup=markup)

# accept callback function
def accept_callback(update: Update, context: CallbackContext):
    # get callback data
    data = update.callback_query.data.split('_')

    data = data[0]

    sender_id = data[1]

    # user id
    user_id = update.callback_query.from_user.id

    # create database object
    db = Database()

    # user name
    user_name = db.get_user(user_id)['first_name']

    # asnwer callback
    update.callback_query.answer('Xabaringiz jonatildi')

    # if user accept
    if data == 'accept':
        # get group id
        group_id = db.get_user(user_id)['group_id']

        # add user to group
        db.add_user_to_group(user_id, group_id)

        # send message to user
        update.callback_query.message.reply_text("Siz guruhga qo'shildingiz")

        # send message to sender
        context.bot.send_message(sender_id, f"{user_name} sizning guruhingizga qo'shildi")

    # if user not accept
    elif data == 'notaccept':
        # send message to user
        update.callback_query.message.reply_text("Siz guruhga qo'shilmadingiz")

        # send message to sender
        context.bot.send_message(sender_id, f"{user_name} sizning guruhingizga qo'shilmadi")

# create queue function
def create_queue(update: Update, context: CallbackContext):
    # save user id
    user_id = update.message.from_user.id

    # create database object
    db = Database()

    # check if user is admin
    if db.check_admin(user_id):
        db.add_queue_all_group()

# create admin
def create_admin(update: Update, context: CallbackContext):
    # save user id
    user_id = update.message.from_user.id

    # get args 
    args = context.args

    # check if args equal to 1717
    if args[0] == '1717':
        # create database object
        db = Database()

        # add admin
        db.add_admin(user_id)

        # send message
        update.message.reply_text("Siz admin oldingiz")

# is_done function
def is_done(update: Update, context: CallbackContext):
    # check is group is done queue then add date to database

    db = Database()
    # check if user is admin
    if db.check_admin(user_id):

        # save user id
        user_id = update.message.from_user.id

        # get args
        args = int(context.args[0])

        today = date.today()
        group_id = db.get_first_group_queue()['group_id']

        db.add_date(today, bool(args), group_id)

def todays_queue(update: Update, context: CallbackContext):
    # check if user is admin
    db = Database()
    
    first, second = db.get_first_queue()

    if first:
        update.message.reply_text(f"Bugungi Navbatchilar\n{first['first_name']} {first['last_name']}\n{second['first_name']} {second['last_name']}")
    else:
        update.message.reply_text('Bugun hech kim navbatchi emas!')
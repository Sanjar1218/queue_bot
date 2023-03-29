import requests
from db import Database
import os

TOKEN = os.environ.get("TOKEN")

db = Database()

# send message to group user send first occurs in queue database table using requets library
def send_message_to_user(user_id, text):
    # send message to group
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={
        "chat_id": user_id,
        "text": text
    })

first, second = db.get_first_queue()

# send message to first user and second user
send_message_to_user(first['user_id'], f"Bugun siz bilan {second['first_name']} navbatchilik kuningiz")
send_message_to_user(second['user_id'], f"Bugun siz bilan {first['first_name']} navbatchilik kuningiz")

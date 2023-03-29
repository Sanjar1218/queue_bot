from tinydb import TinyDB, Query

db = TinyDB('db.json')
# create class that will be used to store data
# this class has user, group, queue, date and admin database tables
class Database:
    def __init__(self):
        self.user = db.table('user')
        self.group = db.table('group')
        self.queue = db.table('queue')
        self.date = db.table('date')
        self.admin = db.table('admin')

    def add_user(self, user_id, username, first_name, last_name):
        self.user.insert({'user_id': user_id, 'username': username, 'first_name': first_name, 'last_name': last_name})

    def add_group(self, user_id):
        '''add group to database'''
        l = len(self.group.all())

        self.group.insert({'group_id': l, 'user_ids': [user_id]})

    


    
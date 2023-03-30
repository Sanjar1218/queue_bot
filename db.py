from tinydb import TinyDB, Query
from datetime import date, timedelta

db = TinyDB('db.json', indent=4, sort_keys=True, separators=(',', ': '))
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

    def add_user_to_group(self, user_id, group_id):
        '''add user to group'''
        self.group.update({'user_ids': Query().user_ids.append(user_id)}, Query().group_id == group_id)

    def add_queue_all_group(self):
        '''add queue to all groups'''
        # get todays date
        today = date.today()
        for i in self.group.all():
            tomorrow = today + timedelta(days=1)

            self.queue.insert({'group_id': i['group_id'], 'day_count': 1, 'day-1': today, 'day-2': tomorrow})

            today = today + timedelta(days=1)

    def add_date(self, date, is_done, group_id):
        '''add date to corresponding group that is queue is done or not'''
        self.date.insert({'date': date, 'is_done': is_done, 'group_id': group_id})

        # if is_done true remove that group from queue
        if is_done:
            self.queue.remove(Query().group_id == group_id)

    def add_admin(self, user_id, password):
        '''add admin to database'''
        # add admin if password equals to 1717
        if password == '1717':
            self.admin.insert({'user_id': user_id})

    def get_user(self, user_id):
        '''get user from database'''
        return self.user.get(Query().user_id == user_id)
    
    def get_group(self, group_id):
        '''get group from database'''
        return self.group.get(Query().group_id == group_id)
    
    def get_queue(self, group_id):
        '''get queue from database'''
        return self.queue.get(Query().group_id == group_id)
    
    def get_date(self, date):
        '''get date from database'''
        return self.date.get(Query().date == date)
    
    def check_admin(self, user_id):
        '''check if user is admin'''
        return self.admin.get(Query().user_id == user_id)
    
    def get_all_users(self):
        '''get all users from database'''
        return self.user.all()
    
    def get_all_groups(self):
        '''get all groups from database'''
        return self.group.all()
    
    def get_all_queues(self):
        '''get all queues from database'''
        return self.queue.all()
    
    def get_first_queue(self):
        '''get first queue from database'''
        group_id = self.queue.all()[0]['group_id']

        first, second = self.group.get(Query().group_id == group_id)['user_ids']

        # get first and second user from database
        first_user = self.get_user(first)
        second_user = self.get_user(second)

        return first_user, second_user
    
    def get_first_group_queue(self):
        '''get first group queue from database'''
        return self.queue.all()[0]
    
    def get_all_dates(self):
        '''get all dates from database'''
        return self.date.all()
    
    def get_all_admins(self):
        '''get all admins from database'''
        return self.admin.all()
    
    def get_all_users_from_group(self, group_id):
        '''get all users from group'''
        return self.group.get(Query().group_id == group_id)['user_ids']
    
    def get_all_dates_from_group(self, group_id):
        '''get all dates from group'''
        return self.date.search(Query().group_id == group_id)
    
    
    
from datetime import date, timedelta
lst_id = [1,2,3,4,5]

d = {}

today = date.today()

# add one day to today

for i in lst_id:
    tomorrow = today + timedelta(days=1)
    d = {'group_id': i, 'day_count': 1, 'day-1': today, 'day-2': tomorrow}
    print(today)
    today = today + timedelta(days=1)
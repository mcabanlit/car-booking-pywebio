from datetime import date, timedelta, datetime
from tinydb import TinyDB, Query
import time
from tinydb import TinyDB, Query
db = TinyDB('db.json')
db.truncate()

users = db.table('USERS')
users.insert({'user_id': 1,
              'name': 'Admin Sample',
              'username': 'admin',
              'password': 'admin',
              'phone': '265888',
              'email': 'alicedi@gmail.com',
              'birthdate': '1993-09-12',
              'user_type': 'admin'})
users.insert({'user_id': 2,
              'name': 'Driver Li',
              'username': 'driver',
              'password': 'driver',
              'phone': '265888',
              'email': 'driverli@gmail.com',
              'birthdate': '1945-23-09',
              'user_type': 'driver'})
users.insert({'user_id': 3,
              'name': 'Pass Enger',
              'username': 'passenger',
              'password': 'passenger',
              'phone': '265888',
              'email': 'passenger@gmail.com',
              'birthdate': '1969-12-12',
              'user_type': 'passenger'})

bookings = db.table('BOOKINGS')
bookings.insert({'booking_id': 1,
                 'username': 'passenger',
                 'name': 'Pass Enger',
                 'date': datetime.now().strftime("%m/%d/%Y"),#string(datetime.date(datetime.now())),
                 'time': datetime.now().strftime("%H:%M"), #string(datetime.time(datetime.now())),
                 'destination': 'Kamputhaw',
                 'remarks': 'No rush',
                 'status': 'new',
                 'assigned_driver': ''})


User = Query()
def search():
    results = users.search(User.user_type == 'admin')
    # results = users.search(users.user_type == 'admin')
    print(len(results))

search()

# User = Query()
#
# def insert():
#     db.insert({'name': 'John', 'age': 28})
#     db.insert({'name': 'Totie', 'age': 25})
#     db.insert({'name': 'Vormyr', 'age': 21, 'city': 'Cebu'})
#
# def search():
#     results = db.search(User.city == 'Cebu')
#     print(results)
#
# db.truncate()
# insert()
# search()
# print(db.all)


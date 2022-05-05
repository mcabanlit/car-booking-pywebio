from datetime import date, timedelta, datetime
from tinydb import TinyDB, Query
import time
from tinydb import TinyDB, Query
db = TinyDB('db.json')
db.truncate()

users = db.table('USERS')
users.insert({'user_id': 1,
              'name': 'Alice Dikya',
              'username': 'admin',
              'password': 'admin',
              'phone': '265888',
              'email': 'alicedi@gmail.com',
              'birthdate': '23/09/1993',
              'user_type': 'admin'})
users.insert({'user_id': 2,
              'name': 'Leni Lu',
              'username': 'leni',
              'password': '12345',
              'phone': '265888',
              'email': 'leni@gmail.com',
              'birthdate': '23/09/1945',
              'user_type': 'driver'})
users.insert({'user_id': 3,
              'name': 'Marcos Ma',
              'username': 'marcos',
              'password': '12345',
              'phone': '265888',
              'email': 'marcos@gmail.com',
              'birthdate': '23/09/1945',
              'user_type': 'passenger'})

bookings = db.table('BOOKINGS')
bookings.insert({'booking_id': 1,
                 'username': 'marcos',
                 'name': 'Test name',
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


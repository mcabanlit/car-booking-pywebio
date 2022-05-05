# A simple script to calculate BMI


import pywebio
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from datetime import date, timedelta, datetime
from tinydb import TinyDB, Query
import time
import re

db = TinyDB('db.json')
User = Query()
users = db.table('USERS')
bookings = db.table('BOOKINGS')


def welcome():
    choose_onboarding = actions('Welcome', ['Login', 'Signup'],
                                help_text='Choose one of the two options to proceed.')

    if choose_onboarding == 'Login':
        login()
    else:
        signup()


def login():
    credentials = input_group("Login to your account", [
        input('Username', name='username', type=TEXT,
              required=True, PlaceHolder="@username"),
        input('Password', name='password', type=PASSWORD,
              required=True, PlaceHolder="Password")
    ])

    results = users.search(User.username == credentials['username'])
    print(results)
    # print(results[0].get("password"))
    if len(results) == 1 and results[0].get("password") == credentials['password']:
        if results[0].get("user_type") == 'admin':
            admin_options(credentials['username'], results[0].get("name"))
        else:
            create_ride(credentials['username'], results[0].get("name"))
    else:
        popup("Invalid username and/or password.", "Redirecting to welcome page.",
              closable=True)
        welcome()
    # if credentials['username'] == 'admin':
    #     create_ride(credentials['username'])
    # else:
    #     create_ride(credentials['username'])


def signup():
    user_data = input_group("Signup", [
        input('Username', name='username', type=TEXT,
              required=True, PlaceHolder="@username", validate=check_username),

        input('Password', name='password', type=PASSWORD,
              required=True, PlaceHolder="Password"),

        input('Confirm Password', name='password_c', type=PASSWORD,
              required=True, PlaceHolder="Confirm Password"),

        input('Name', name='name', type=TEXT, required=True,
              PlaceHolder="name"),

        input('Phone', name='phone', type=NUMBER,
              required=True, PlaceHolder="12345"),

        input('Email', name='email', type=TEXT,
              required=True, PlaceHolder="user@gmail.com"),

        input('Birthdate: ', name='birthdate', type=DATE,
              PlaceHolder="23/09/1993"),

    ], validate=check_form)

    # Create a checkbox
    agree = checkbox("Agreement", options=[
        'I agree to terms and conditions'], required=True)

    # Display output using popup
    # popup("Your Details",
    #       f"Username: @{user_data['username']}\nName: {user_data['name']}\
    #       \nPhone: {str(user_data['phone'])}\nEmail: {user_data['email']}",
    #       closable=True)
    print(agree)
    if agree[0] == 'I agree to terms and conditions':
        create_ride(user_data['username'], user_data['name'])

def admin_options(username, name):
    admin_task = actions('Welcome Admin @{username}', ['View all bookings', 'Book a ride for myself'],
                                help_text='Choose one of the two options to proceed.')

    if admin_task == 'Book a ride for myself':
        create_ride(username, name)
    else:
        display_table = [['Name', 'User ID', 'Date', 'Time','Destination','Remarks','Status', 'Driver']]
        for row in bookings:
            display_table.append( [
                row['name'], row['username'],
                row['date'], row['time'], row['destination'], row['remarks'], row['status'], row['assigned_driver']])

            print(row)

        put_table(display_table)
        put_buttons([dict(label='Home', value='s', color='success')], onclick=admin_options(username, name))




def check_form(user_data):
    # For checking Email, whether Valid or not.
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    # for checking Name
    if user_data['name'].isdigit():
        return ('name', 'Invalid name!')

    # for checking Email
    if not (re.search(regex, user_data['email'])):
        return ('email', 'Invalid email!')

    # for matching Passwords
    if user_data['password'] != user_data['password_c']:
        return ('password_c', "Please make sure your passwords match.")


def create_ride(username, name):
    ride_details = input_group("Create a Ride Request", [
        input('Name: ', name='name', placeholder='First, Last', value = name),
        input('User ID: ', name='username', readonly=True, placeholder=username, value=username),
        input('Date: ', name='booking_date', type=DATE, validate=check_booking_date, value = datetime.now().strftime("%Y-%m-%d")),
        input('Time: ', name='booking_time', type=TIME, value = datetime.now().strftime("%H:%M")),
        input('Ride Destination:', name='booking_destination'),
        input('Remarks:', name='booking_remarks')
    ])

    print(ride_details['booking_date'], ride_details['booking_time'])

    bookings.insert({'booking_id': 1,
                     'username': ride_details['username'],
                     'name': ride_details['name'],
                     'date': ride_details['booking_date'],  # string(datetime.date(datetime.now())),
                     'time': ride_details['booking_time'],  # string(datetime.time(datetime.now())),
                     'destination': ride_details['booking_destination'],
                     'remarks': ride_details['booking_remarks'],
                     'status': 'new',
                     'assigned_driver': ''})

    popup("Ride request succesfully sent.",
          f"A rider will contact you shortly. \n \n \nRide details:\nName: @{ride_details['username']}\nName: {ride_details['name']}\
                \nDate: {str(ride_details['booking_date'])}\nTime: {ride_details['booking_time']}\
                \nDestination: {ride_details['booking_destination']}\
                \nRemarks: {ride_details['booking_remarks']}",
          closable=True)


    create_ride(username, name)

def show_ride_request(ride_details):
    put_table([['Name', 'User ID', 'Date', 'Time'], [
        ride_details['name'], ride_details['username'],
        ride_details['booking_date'], ride_details['booking_time']]])


def check_username(username):
    results = users.search(User.username == username)
    if len(results) > 0:
        return 'Choose another username.'


def check_booking_date(booking_date):
    entered_day = datetime.strptime(booking_date, "%Y-%m-%d")
    present_day = datetime.now()
    if entered_day.date() < present_day.date():
        return 'Choose a better date'


def set_now_ts(set_value):
    set_value(int(time.time()))


def select_date(set_value):
    with popup('Select Date'):
        put_buttons(['Today'], onclick=[lambda: set_value(date.today(), 'Today')])
        put_buttons(['Yesterday'], onclick=[lambda: set_value(date.today() - timedelta(days=1), 'Yesterday')])


def bmi():
    height = input("Input your height(cm)：", type=FLOAT)
    weight = input("Input your weight(kg)：", type=FLOAT)

    BMI = weight / (height / 100) ** 2

    top_status = [(16, 'Severely underweight'), (18.5, 'Underweight'),
                  (25, 'Normal'), (30, 'Overweight'),
                  (35, 'Moderately obese'), (float('inf'), 'Severely obese')]

    for top, status in top_status:
        if BMI <= top:
            put_markdown('# **Results**')
            put_text('Your BMI: %.1f. Category: %s' % (BMI, status))
            put_html('<br><br>')
            put_markdown('Your BMI: `%.1f`. Category: `%s`' % (BMI, status))
            put_html('<hr>')
            put_table([
                ['Your BMI', 'Category'],
                [BMI, status],
            ])

            break


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-p", "--port", type = int, default = 8080)
#     args = parser.parse_args()
#
#     start_server(welcome, port = args.port)

# Uncomment when running in local
if __name__ == '__main__':
    pywebio.start_server(welcome, port=55)

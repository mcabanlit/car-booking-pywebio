import pywebio
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from datetime import date, timedelta, datetime
from tinydb import TinyDB, Query
from functools import partial
import time
import re
import argparse

# Initialize Flask object
app = Flask(__name__)

# Initialize TinyDB
db = TinyDB('db.json')
User = Query()
users = db.table('USERS')
bookings = db.table('BOOKINGS')


def welcome():
    """
    Car Booking Application

    Displays the welcome options for the car booking app. Would require users to either login or signup.

    Returns:
            None
    """

    # Choose from either login or signup
    choose_onboarding = actions('Welcome to Car Booking App', ['Login', 'Signup'],
                                help_text='Choose one of the options to proceed.')

    if choose_onboarding == 'Login':
        login()
    else:
        signup()


def login():
    '''
    Login options for existing users.

    Returns:
            None
    '''
    credentials = input_group("Login to your account", [
        input('Username', name='username', type=TEXT,
              required=True, PlaceHolder="@username"),
        input('Password', name='password', type=PASSWORD,
              required=True, PlaceHolder="Password")
    ])

    # Checks for existing users that matches the username
    results = users.search(User.username == credentials['username'])
    print(results)

    # Checks the password and the user type
    if len(results) == 1 and results[0].get("password") == credentials['password']:
        if results[0].get("user_type") == 'admin':
            admin_options(credentials['username'], results[0].get("name"))
        elif results[0].get("user_type") == 'driver':
            driver_options(credentials['username'], results[0].get("name"))
        else:
            user_options(credentials['username'], results[0].get("name"))
    else:
        popup("Invalid username and/or password.", "Redirecting to welcome page.",
              closable=True)
        welcome()


def signup():
    """
    Sign up page / option for new users.

    Returns:
            None
    """

    # Input user credentials
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

    # Create a radio button asking for user type
    user_type = radio("User Type", options=['Driver', 'Passenger'], required=True)
    user_type = user_type.lower()

    # Create a checkbox for agreeing with terms and conditions
    agree = checkbox("Agreement", options=[
        'I agree to terms and conditions'], required=True)

    # Display output using popup
    # popup("Your Details",
    #       f"Username: @{user_data['username']}\nName: {user_data['name']}\
    #       \nPhone: {str(user_data['phone'])}\nEmail: {user_data['email']}",
    #       closable=True)
    print(agree)
    if agree[0] == 'I agree to terms and conditions':
        last_row = users.get(doc_id=len(users))
        print(last_row["user_id"])
        new_user_id = int(last_row["user_id"]) + 1
        users.insert({'user_id': new_user_id,
                         'username': user_data['username'],
                         'name': user_data['name'],
                         'password': user_data['password'],
                         'phone': user_data['phone'],
                         'email': user_data['email'],
                         'birthdate': user_data['birthdate'],
                         'user_type': user_type})

        # Proceed to specific options per user but if the user is
        # not a driver, then proceed to creating a ride.
        if user_type == 'driver':
            driver_options(user_data['username'], user_data['name'])
        else:
            create_ride(user_data['username'], user_data['name'])
            user_options(user_data['username'], user_data['name'])


def driver_options(username, name):
    """
    Options for user type: driver
    The drivers are allowed to
        (1) View all new bookings (status = new)
        (2) View their accepted bookings (driver = @username)
        (3) View finished bookings (status = done and driver = @username)
        (4) Book a ride for themselves

    Parameters:
        username (string): username of the user in session
        name (string): Their full name in the form

    Returns:
        None
    """
    admin_task = actions(f'Welcome Driver @{username}', ['View all bookings', 'View my bookings', 'View finished bookings', 'Book a ride for myself', 'Logout'],
                                help_text='Choose one of the options to proceed.')
    # put_buttons([dict(label='Home', value='s', color='success')], onclick=admin_options(username, name))

    if admin_task == 'Book a ride for myself':
        clear()
        create_ride(username, name)
        driver_options(username, name)
    elif admin_task == 'Logout':
        clear()
        welcome()
    elif admin_task == 'View all bookings':
        clear()
        display_table = [['Name', 'User ID', 'Date', 'Time', 'Destination', 'Remarks', 'Status', 'Driver', 'Action']]
        for row in bookings:
            if row['status'] == 'new':
                display_table.append([
                    row['name'], row['username'],
                    row['date'], row['time'], row['destination'], row['remarks'], row['status'],
                    row['assigned_driver'],
                    put_buttons(['Accept Booking'], onclick=partial(update_driver, row=row, username=username, name=name))])

                print(row)
        # put_buttons([dict(label='Home', value='s', color='success')], onclick=admin_options(username, name))
        put_table(display_table)
        driver_options(username, name)
    elif admin_task == 'View my bookings':
        clear()
        display_table = [['Name', 'User ID', 'Date', 'Time', 'Destination', 'Remarks', 'Status', 'Driver', 'Action']]
        for row in bookings:
            if row['assigned_driver'] == username and row['status'] != 'done':
                display_table.append([
                    row['name'], row['username'],
                    row['date'], row['time'], row['destination'], row['remarks'], row['status'], row['assigned_driver'],
                    put_buttons(['Mark as Done'], onclick=partial(update_status, row=row, username=username, name=name))])

                print(row)
        # put_buttons([dict(label='Home', value='s', color='success')], onclick=admin_options(username, name))
        put_table(display_table)

        driver_options(username, name)
    elif admin_task == 'View finished bookings':
        clear()
        display_table = [['Name', 'User ID', 'Date', 'Time','Destination','Remarks','Status', 'Driver']]
        for row in bookings:
            if row['assigned_driver'] == username and row['status'] == 'done':
                display_table.append( [
                    row['name'], row['username'],
                    row['date'], row['time'], row['destination'], row['remarks'], row['status'], row['assigned_driver']])

                print(row)
        # put_buttons([dict(label='Home', value='s', color='success')], onclick=admin_options(username, name))
        put_table(display_table)

        driver_options(username, name)


def update_driver(choice, row, username, name):
    """
    Update the driver of a particular booking.
    When the driver clicks on the Accept Booking button, this function would
    update the assigned driver.

    Parameters:
        choice (string): the choice or name of the button that was clicked
        row (dictionary): the whole row of the booking that needs updating
        username (string): username of the user in session
        name (string): their full name in the form

    Returns:
        None
    """

    put_text("You click %s button ar row %s" % (choice, row))
    bookings.update({'assigned_driver': username, 'status': 'booked'}, User.booking_id == row['booking_id'])
    toast(f"Marked as booked for driver @{username}.")
    # username = row['username']
    # name = row['name']
    print(username,name)
    clear()
    display_table = [['Name', 'User ID', 'Date', 'Time', 'Destination', 'Remarks', 'Status', 'Driver', 'Action']]
    for row in bookings:
        if row['status'] == 'new':
            display_table.append([
                row['name'], row['username'],
                row['date'], row['time'], row['destination'], row['remarks'], row['status'],
                row['assigned_driver'],
                put_buttons(['Book'], onclick=partial(update_driver, row=row, username=username, name=name))])

            print(row)
    # put_buttons([dict(label='Home', value='s', color='success')], onclick=admin_options(username, name))
    put_table(display_table)

    driver_options(username, name)



def update_status(choice, row, username, name):
    put_text("You click %s button ar row %s" % (choice, row))
    bookings.update({'status': 'done'}, User.booking_id == row['booking_id'])
    toast("Marked as done.")
    # username = row['username']
    # name = row['name']
    print(username,name)
    clear()
    display_table = [['Name', 'User ID', 'Date', 'Time', 'Destination', 'Remarks', 'Status', 'Driver', 'Action']]
    for row in bookings:
        if row['assigned_driver'] == username and row['status'] != 'done':
            display_table.append([
                row['name'], row['username'],
                row['date'], row['time'], row['destination'], row['remarks'], row['status'], row['assigned_driver'],
                put_buttons(['Done'], onclick=partial(update_status, row = row, username = username, name = name))])

            print(row)
    # put_buttons([dict(label='Home', value='s', color='success')], onclick=admin_options(username, name))
    put_table(display_table)
    driver_options(username, name)


def user_options(username, name):
    admin_task = actions(f'Welcome User @{username}', ['View my bookings', 'Book a ride for myself', 'Logout'],
                                help_text='Choose one of the options to proceed.')
    # put_buttons([dict(label='Home', value='s', color='success')], onclick=admin_options(username, name))

    if admin_task == 'Book a ride for myself':
        clear()
        create_ride(username, name)
        user_options(username, name)
    elif admin_task == 'Logout':
        clear()
        welcome()
    else:
        clear()
        display_table = [['Name', 'User ID', 'Date', 'Time','Destination','Remarks','Status', 'Driver', 'Action']]
        for row in bookings:
            if row['username'] == username:
                display_table.append([
                    row['name'], row['username'],
                    row['date'], row['time'], row['destination'], row['remarks'], row['status'], row['assigned_driver'],
                    put_buttons(['Cancel Request'], onclick=partial(cancel_request, row=row, username=username, name=name))])

                print(row)
        # put_buttons([dict(label='Home', value='s', color='success')], onclick=admin_options(username, name))
        put_table(display_table)

        user_options(username, name)

def cancel_request(choice, row, username, name):
    # put_text("You click %s button ar row %s" % (choice, row))
    results = users.search(User.username == username)
    user_type = ''
    if len(results) > 0:
        user_type = results[0].get("user_type")
    print("User " + user_type)
    if user_type == 'passenger':
        bookings.update({'status': 'cancelled by user'}, User.booking_id == row['booking_id'])
    elif user_type == 'admin':
        bookings.update({'status': 'cancelled by admin'}, User.booking_id == row['booking_id'])

    toast("Booking request cancelled.")
    # username = row['username']
    # name = row['name']
    print(username, name)
    clear()

    if user_type == 'passenger':
        user_options(username, name)
    elif user_type == 'admin':
        admin_options(username, name)


def admin_options(username, name):
    admin_task = actions(f'Welcome Admin @{username}', ['View all bookings', 'View all users','Book a ride for myself', 'Logout'],
                                help_text='Choose one of the options to proceed.')
    # put_buttons([dict(label='Home', value='s', color='success')], onclick=admin_options(username, name))

    if admin_task == 'Book a ride for myself':
        clear()
        create_ride(username, name)
        admin_options(username, name)
    elif admin_task == 'Logout':
        clear()
        welcome()
    elif admin_task == 'View all users':
        clear()
        display_table = [['ID', 'Name', 'Username', 'Phone', 'Email', 'Birthdate', 'User Type']]
        for row in users:
            display_table.append([
                row['user_id'], row['name'],
                row['username'], row['phone'], row['email'], row['birthdate'], row['user_type']])

            print(row)
        # put_buttons([dict(label='Home', value='s', color='success')], onclick=admin_options(username, name))
        put_table(display_table)

        admin_options(username, name)
    else:
        clear()
        display_table = [['Name', 'User ID', 'Date', 'Time','Destination','Remarks','Status', 'Driver', 'Action']]
        for row in bookings:
            display_table.append( [
                row['name'], row['username'],
                row['date'], row['time'], row['destination'], row['remarks'], row['status'], row['assigned_driver'],
                put_buttons(['Cancel Request'],onclick=partial(cancel_request, row=row, username=username, name=name))])

            print(row)
        # put_buttons([dict(label='Home', value='s', color='success')], onclick=admin_options(username, name))
        put_table(display_table)

        admin_options(username, name)




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
    # print(bookings[len(bookings)]["booking_id"])
    last_row = bookings.get(doc_id=len(bookings))
    print(last_row["booking_id"])
    new_booking_id = int(last_row["booking_id"]) + 1
    ride_details = input_group("Create a Ride Request", [
        input('Name: ', name='name', placeholder='First, Last', value = name),
        input('User ID: ', name='username', readonly=True, placeholder=username, value=username),
        input('Date: ', name='booking_date', type=DATE, validate=check_booking_date, value = datetime.now().strftime("%Y-%m-%d")),
        input('Time: ', name='booking_time', type=TIME, value = datetime.now().strftime("%H:%M")),
        input('Ride Destination:', name='booking_destination'),
        input('Remarks:', name='booking_remarks')
    ])

    print(ride_details['booking_date'], ride_details['booking_time'])

    bookings.insert({'booking_id': new_booking_id,
                     'username': ride_details['username'],
                     'name': ride_details['name'],
                     'date': ride_details['booking_date'],  # string(datetime.date(datetime.now())),
                     'time': ride_details['booking_time'],  # string(datetime.time(datetime.now())),
                     'destination': ride_details['booking_destination'],
                     'remarks': ride_details['booking_remarks'],
                     'status': 'new',
                     'assigned_driver': ''})

    popup("Ride request succesfully sent.",
          f"A rider will contact you shortly. \n \n \nRide details:\nUsername: @{ride_details['username']}\nName: {ride_details['name']}\
                \nDate: {str(ride_details['booking_date'])}\nTime: {ride_details['booking_time']}\
                \nDestination: {ride_details['booking_destination']}\
                \nRemarks: {ride_details['booking_remarks']}",
          closable=True)


    # create_ride(username, name)

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




# Uncomment when running in local
# if __name__ == '__main__':
#     pywebio.start_server(welcome, port=7171)


# app.add_url_rule('/booking', 'webio_view', webio_view(welcome), methods=['GET', 'POST', 'OPTIONS'])


# app.run(host='localhost', port=80)

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-p", "--port", type=int, default=8080)
#     args = parser.parse_args()
#
#     start_server(welcome, port=args.port)


app.add_url_rule('/tool', 'webio_view', webio_view(welcome),
            methods=['GET', 'POST', 'OPTIONS'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(welcome, port=args.port)
# A simple script to calculate BMI
import argparse

import pywebio
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from datetime import date, timedelta, datetime
import time

def welcome():
    login_type = radio("Gender", options=['New Account', 'I already have an acount'])
    if login_type == 'New Account':
        signup()
    else:
        login()
def login():
    credentials = input_group("Login to your account", [
        input('Username', name='username', type=TEXT,
              required=True, PlaceHolder="@username"),

        input('Password', name='password', type=PASSWORD,
              required=True, PlaceHolder="Password")
    ])

    if credentials['username'] == 'admin':
        create_ride(credentials['username'])

def signup():
    user_data = input_group("Signup", [
        input('Username', name='username', type=TEXT,
              required=True, PlaceHolder="@username"),

        input('Password', name='pass', type=PASSWORD,
              required=True, PlaceHolder="Password"),

        input('Confirm Password', name='passes', type=PASSWORD,
              required=True, PlaceHolder="Confirm Password"),

        input('Name', name='name', type=TEXT, required=True,
              PlaceHolder="name"),

        input('Phone', name='phone', type=NUMBER,
              required=True, PlaceHolder="12345"),

        input('Email', name='email', type=TEXT,
              required=True, PlaceHolder="user@gmail.com"),

        input('Birthdate: ', name='birthdate', type=DATE,
              PlaceHolder="23/09/1993"),

    ])

    # Create a checkbox
    agree = checkbox("Agreement", options=[
        'I agree to terms and conditions'], required=True)

    # Display output using popup
    popup("Your Details",
          f"Username: @{user_data['username']}\nName: {user_data['name']}\
          \nPhone: {str(user_data['phone'])}\nEmail: {user_data['email']}",
          closable=True)

    create_ride(user_data['username'])

def create_ride(username):
    ride_details = input_group("Create a Ride Request", [
        input('Name: ', name='name', placeholder= 'First, Last'),
        input('User ID: ', name= 'username', readonly = True, placeholder= username, value=username),
        input('Date: ', name = 'booking_date', type = DATE, validate= check_booking_date),
        input('Time: ', name='booking_time', type= TIME),
        input('Ride Destination:', name='booking_destination'),
        input('Remarks:', name = 'booking_remarks')
    ])

    show_ride_request(ride_details)

def show_ride_request(ride_details):
    put_table([['Name', 'User ID', 'Date', 'Time'],[
               ride_details['name'], ride_details['username'],
               ride_details['booking_date'], ride_details['booking_time']]])

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type = int, default = 8080)
    args = parser.parse_args()

    start_server(welcome, port = args.port)

# Uncomment when running in local
# if __name__ == '__main__':
#     pywebio.start_server(welcome, port=55)
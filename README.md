## Car Booking Web App [![gcash donation][1]][2] [![paypal donation][3]][4]

[![license][5]][6] [![python version][7]][8] [![pywebio version][9]][10] [![build][11]][12] 

Car booking web app implemented using `PyWebIO` and `TinyDB`. <br />
PyWebIO is a rich text terminal and can be used to build simple web applications or browser-based GUI applications. TinyDB is a very tiny database that stores all the data as a Python dictionary. <br />

You will be asked to either login or sign up for a new account.
![image](https://user-images.githubusercontent.com/102983286/172987911-c2857f92-f6fa-425d-9442-26c0c338e853.png)


There are three main user types:
1. Passenger
2. Driver
3. Admin

You may signup for the first two user types (passenger and driver), but if you require admin access, you may use the below:<br />
_Username:_ `admin` <br />
_Password:_ `admin` <br />

For testing of the other two user types, you may use the below accordingly: <br />
Driver User <br />
_Username:_ `driver` <br />
_Password:_ `driver` <br />

Passenger User <br />
_Username:_ `passenger` <br />
_Password:_ `passenger` <br />

Here is the signup page for reference:
![image](https://user-images.githubusercontent.com/102983286/167591247-ac2b09dc-5597-4a57-bf27-e75383cf2f19.png)

There is currenly no session handling being implemented in the code so refreshing the page will log you out.
Each user type has a different set of options.

1. Passenger
* ![image](https://user-images.githubusercontent.com/102983286/168568203-23e14d71-1fe3-403c-92e2-0062f8117696.png)
2. Driver
* ![image](https://user-images.githubusercontent.com/102983286/167591721-6d4eaf34-4a9e-4228-af54-651ad20651cd.png)
3. Admin
* ![image](https://user-images.githubusercontent.com/102983286/167591613-3d1d37e9-2743-42a8-994b-ae178dccc7d0.png)

Thank you and please bare with my newbie Python web skills.

[1]: https://img.shields.io/badge/donate-gcash-green
[2]: https://drive.google.com/file/d/1JeMx5_S7VBBT-3xO7mV9YOMfESeV3eKa/view

[3]: https://img.shields.io/badge/donate-paypal-blue
[4]: https://www.paypal.com/paypalme/mcabanlitph

[5]: https://img.shields.io/badge/license-GNUGPLv3-blue.svg
[6]: https://github.com/mcabanlit/heart-disease/blob/main/LICENSE.md

[7]: https://img.shields.io/badge/python-3.10-blue
[8]: https://www.python.org/

[9]: https://img.shields.io/badge/pywebio-1.6.1-dark
[10]: https://pywebio.readthedocs.io/en/latest/

[11]: https://img.shields.io/badge/build-passing-green
[12]: https://car-booking-pywebio.herokuapp.com/

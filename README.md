## Car Booking Web App 
Car booking web app implemented using `PyWebIO` and `TinyDB`. <br />
PyWebIO is a rich text terminal and can be used to build simple web applications or browser-based GUI applications. TinyDB is a very tiny database that stores all the data as a Python dictionary. <br />
_Note: This app has not been successfully deployed to Heroku and Vercel._

You may run index.py from the root folder in your local for now. 
You will be asked to either login or sign up for a new account.
![image](https://user-images.githubusercontent.com/102983286/167590144-674b0519-1720-459e-933f-396723d87a7c.png)

There are three main user types:
1. Passenger
2. Driver
3. Admin

You may signup for the first two user types, but if you require admin access, you may use the below:<br />
_Username:_ `admin` <br />
_Password:_ `admin` <br />

For the other two user types, you may use the below accordingly:
Driver User
_Username:_ `driver` <br />
_Password:_ `driver` <br />

Passenger User
_Username:_ `passenger` <br />
_Password:_ `passenger` <br />

Here is the signup page for reference:
![image](https://user-images.githubusercontent.com/102983286/167591247-ac2b09dc-5597-4a57-bf27-e75383cf2f19.png)

There is currenly no session handling being implemented in the code so refreshing the page will log you out.
Each user type has a different set of options.

1. Passenger
* ![image](https://user-images.githubusercontent.com/102983286/167591577-bc98e004-368d-4530-a92d-2953da291647.png)
2. Driver
* ![image](https://user-images.githubusercontent.com/102983286/167591721-6d4eaf34-4a9e-4228-af54-651ad20651cd.png)
3. Admin
* ![image](https://user-images.githubusercontent.com/102983286/167591613-3d1d37e9-2743-42a8-994b-ae178dccc7d0.png)

Thank you and please bare with my newbie Python web skills.

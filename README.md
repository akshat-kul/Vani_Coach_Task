# Vani_Coach_Task

Using Flask and PostgreSQL.

# Initial process
1) Firstly a Login-Signup system is added.
2) User can register using "/signup" endpoint through mobile number.
3) After registering, they can generate the OTP to complete the verification process. This can be done through "/generate_otp" and with this endpoint user can generate OTP and receive it on their registered mobile number.
4) In the final verification process, user have to enter received OTP on "/login" endpoint to complete the verification process. Additionally they can use the features of the app.

# Differentiating between Admin Role & User Role
1) While signing up, user can assign themselves as admin role and with that they'll be able to utilise features that are hidden to commercial users.
2) To stop giving access to hidden endpoint, jwt_token() is required. And without that token user cannot get access to all the hidden endpoints. 
3) To get the jwt_token, while logging, user has to have admin role and then only they can receive jwt token to access the additional features

# Features Accessible to Admin
1) Admin can add vehicles
2) Admin can add vehicle stations
3) Admin can assign multiple vehicles to different stations

# Features Accessible to User
1) User can retrieve the list of vehicles at particular station
2) User can place an order for a vehicle from a station. Only available vehicles at that station can be ordered.
3) User can return the picked-up vehicle to any station with the order_id they have got while placing a new order entry.

# Endpoints available
1) "/" --> homepage
2) "/signup" --> For signing-up
3) "/generate_otp" --> For generating OTP to initialise the verification process
4) "/login" --> Logging in as user or admin
5) "/create_vehicle" --> For adding the new vehicle in the table. Only accessible by admin.
6) "/create_vehicle_station" --> For adding the new vehicle station in the table. Only accessible by admin.
7) "/inventory" --> For assinging the multiple vehicles to a particular station. Onyl accessible by admin.
8) "/retrieve_vehicles" --> For fetching the list of different vehicles at a station.
9) "/order_vehicle" --> For placing the pickup order of a vehicle from a station with the available vehicles.
10) "/return_vehicle" --> For placing the return order of a vehicle to any possible station.

# Endpoints that should be hidden from frontend
1) "/create_vehicle"
2) "/create_vehicle_station"
3) "/inventory"

#Testing
It can be tested easily using Postman 
Localhost URL: http://127.0.0.1:5000/

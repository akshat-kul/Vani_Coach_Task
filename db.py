from functools import wraps
import jwt
from sqlalchemy import exists, null, MetaData
from models import UserReturn, Users, CarDetails, StationDetails, Inventory, UserPickup, Base, session, engine
from flask import Flask, jsonify, request

from twilio.rest import Client
import random
from datetime import date, datetime, timedelta
import pandas as pd

app = Flask(__name__)

account_sid = 'AC195ca26bfdfdbb412301a5adf85432c7'
auth_token = '9471aef11f82bcec6c062877602799ca'
client = Client(account_sid, auth_token)


def mk_session(fun):
    def wrapper(*args, **kwargs):
        s = session()
        kwargs['session'] = s
        try:
            res = fun(*args, **kwargs)
        except Exception as e:
            s.rollback()
            s.close()
            raise e

        s.close()
        return res
    wrapper.__name__ = fun.__name__
    return wrapper

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = Users.query.filter_by(public_id=data['public_id']).first()
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
   return decorator

#For Inserting Users to table
@mk_session
def dbInsertUser(username, mob_number, role, session=None):
    if role=="customer":
        role1 = 0
    elif role=="admin":
        role1 = 1
    new_user = Users(username=username, mobile_number=mob_number, admin=role1, signup_date= getCurrentTime())
    session.add(new_user)
    session.commit()
    return jsonify({"message":"New User created"})

#For Login and verifiying the user
@mk_session
def dbLogin(mob_number, otp, session=None): 
    query = session.query(Users).filter(Users.mobile_number==mob_number).statement
    df = pd.read_sql( query, engine)
    print(df)
    if(df.empty):
        flag=1
        return flag
    else:
        df['status_verified']  = True
        df.to_sql("user_details", engine, if_exists="replace")
        return "Account verified successfully"

#For inserting vehicles in database. Only can be done by admin
@mk_session
def insert_vehicle(data, session=None):
    new_vehicle = CarDetails(car_name = data['car_name'], car_class_name = data['car_class'], total_cars = data['quantity'])
    session.add(new_vehicle)
    session.commit()
    return "Details Successfully entered!!"

#For Uploading stations in database. Only can be done by admin
@mk_session
def insert_vehicle_station(data, session=None):
    new_vehicle_station = StationDetails(station_name = data['station_name'])
    session.add(new_vehicle_station)
    session.commit()
    return "Details Successfully entered!!"

#For assigning vehicles to different stations. It can be done only by admin
@mk_session
def assign_vehicle(data, session=None):
    assign_vehicle_station = Inventory(station_id = data['station_id'], car_id = data['car_id'])
    session.add(assign_vehicle_station)
    session.commit()
    return "Details Successfully entered!!"

#Retrieving the list of vehicles on a particular station
@mk_session
def vehicles_list(data, session=None):
    vehicle_dict = {}
    vehicle_list = []
    query = session.query(Inventory).filter(Inventory.station_id==data['station_id']).statement
    df = pd.read_sql( query, engine)
    query = session.query(StationDetails).filter(StationDetails.id==int(df.at[0,'station_id'])).statement
    df1 = pd.read_sql(query,engine)
    for i in range(len(df.at[0,'car_id'])):
        query = session.query(CarDetails).filter(CarDetails.id==int(df.at[0,'car_id'][i])).statement
        df2 = pd.read_sql(query,engine)
        vehicle_list.append(df2.loc[0,'car_name'])
    vehicle_dict = {"Station Name": df1.at[0,'station_name'], "Cars Available": vehicle_list}
    return vehicle_dict    

#Placing the order for a vehicle from a particular station
@mk_session
def place_order(data, session=None):
    query = session.query(Inventory).filter(Inventory.station_id==data['station_id']).statement
    df = pd.read_sql( query, engine)
    if df.empty:
        detail = {"message":"Wrong Station ID is entered!!"}
    else:
        if data['car_id'] not in df.at[0,'car_id']:
            detail = {"message":"Wrong Car ID is entered!!"}
        else:
            order_id = random.randint(1,1000)
            pickup_order = UserPickup(order_id = order_id,pickup_station_id = data['station_id'], pickup_car_id = data['car_id'], pickup_time = getCurrentTime())
            session.add(pickup_order)
            session.commit()
            query = session.query(StationDetails).filter(StationDetails.id==data['station_id']).statement
            df1 = pd.read_sql(query,engine)
            query = session.query(CarDetails).filter(CarDetails.id==data['car_id']).statement
            df2 = pd.read_sql(query,engine)
            detail = {"Station_Name": df1.at[0,'station_name'], "Car Name": df2.at[0,'car_name'], "Order ID": order_id}
    return detail

#Returning the picked up vehicle to any station
@mk_session
def return_order(data, session=None):
    query = session.query(UserPickup).filter(UserPickup.order_id==data['order_id']).statement
    df = pd.read_sql( query, engine)
    print(df)
    if df.empty:
        detail = {"message":"Wrong Station ID is entered!!"}
    else:
        return_order = UserReturn(order_id = data['order_id'],return_station_id = data['station_id'], pickup_car_id = int(df.at[0,'pickup_car_id']), return_time = getCurrentTime())
        session.add(return_order)
        session.commit()
        query = session.query(StationDetails).filter(StationDetails.id==data['station_id']).statement
        df1 = pd.read_sql(query,engine)
        query = session.query(CarDetails).filter(CarDetails.id==int(df.at[0,'pickup_car_id'])).statement
        df2 = pd.read_sql(query,engine)
        detail = {"Station_Name": df1.at[0,'station_name'], "Car Name": df2.at[0,'car_name']}
    return detail


def getCurrentTime():
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_time_str

@mk_session
def generateOTP(mob_number, session=None):
    query = session.query(Users).filter(Users.mobile_number==mob_number).statement
    df = pd.read_sql( query, engine)
    print(df)
    if(df.empty):
        flag=1
        return flag
    else:
        global otp_main
        otp_main = random.randint(1000,9999)
        message = client.messages.create(
         body='Hello!! Your OTP is - ' + str(otp_main) + '.',
         from_='+17632972882',
         to=mob_number
        )
        print(message.sid)
        print("OTP is ",otp_main)
        flag=0
        return otp_main


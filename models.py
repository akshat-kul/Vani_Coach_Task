from sqlalchemy import ARRAY, create_engine, Boolean, TIMESTAMP, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://postgres:admin@localhost/postgres"

Base = declarative_base()

engine = create_engine(DB_URL, pool_recycle=3600, connect_args={'connect_timeout': 60})
session = sessionmaker(bind=engine)

class Users(Base):
    __tablename__ = 'user_details'
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    mobile_number = Column(String(13), unique=True)
    status_verified = Column(Boolean, default=False)
    admin = Column(Boolean)
    signup_date = Column(TIMESTAMP)

class CarDetails(Base):
    __tablename__ = 'car_detail'
    id = Column(Integer, primary_key = True, autoincrement=True)
    car_name = Column(String)
    car_class_name = Column(String)
    #total_cars = Column(Integer)
    
class StationDetails(Base):
    __tablename__ = 'station_details'
    id = Column(Integer, primary_key =True)
    station_name = Column(String)

class Inventory(Base):
    __tablename__ = 'inventory_details'
    id = Column(Integer, primary_key =True)
    car_id = Column(ARRAY(Integer))
    station_id = Column(Integer,ForeignKey(StationDetails.id))

class UserPickup(Base):
    __tablename__ = 'order_detail'
    id = Column(Integer, primary_key =True)
    order_id = Column(Integer)
    #user_id = Column(Integer, ForeignKey(Users.id))
    pickup_station_id = Column(Integer, ForeignKey(StationDetails.id))
    pickup_car_id = Column(Integer, ForeignKey(CarDetails.id))
    return_status = Column(Boolean, default=False)
    pickup_time = Column(TIMESTAMP)

class UserReturn(Base):
    __tablename__ = 'return_detail'
    id = Column(Integer, primary_key =True)
    order_id = Column(Integer)
    #user_id = Column(Integer, ForeignKey(Users.id))
    return_station_id = Column(Integer, ForeignKey(StationDetails.id))
    pickup_car_id = Column(Integer, ForeignKey(CarDetails.id))
    return_status = Column(Boolean, default=True)
    return_time = Column(TIMESTAMP)

Base.metadata.create_all(engine)

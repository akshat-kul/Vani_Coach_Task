from flask_bcrypt import Bcrypt
from flask import Flask, jsonify, render_template, request
from flask_restful import Api
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from db import assign_vehicle, dbInsertUser, dbLogin, generateOTP, insert_vehicle, insert_vehicle_station, place_order, return_order, vehicles_list

app = Flask(__name__, template_folder='template', static_folder='staticFiles')
api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = "root"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/postgres"

#Homepage
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

#Signup
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        mob_number = request.form.get("mobile_number")
        role = request.form.get("role")
        dbInsertUser(username, mob_number, role)
        return render_template('generate_otp.html')
    return render_template('signup.html'),"Data Successfully Inserted in Database"

#URL for generating OTP
@app.route('/generate_otp', methods=["GET", "POST"])
def generate_otp():
    if request.method == "POST":
        mob_number = request.form.get("mob_number")
        flag = generateOTP(mob_number)
        if flag==1:
            return render_template('generate_otp.html')
        else:
            return render_template('login.html')
    return render_template('generate_otp.html')

#Login
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        mob_number = request.form.get("mob_number")
        otp = request.form.get('otp')
        flag = dbLogin(mob_number,otp)
        if flag==1:
            return render_template('login.html')
        else:
            token = create_access_token(identity=mob_number)
            print(token)
            return render_template('profile.html')
    return render_template('login.html')

#Creating vehicle
@app.route('/create_vehicle', methods=['POST'])
@jwt_required()
def create_vehicle():
    data = request.get_json()
    insert_vehicle(data)
    return jsonify({"message":"Car Details Successfully Inserted"}, data)

#Creating Stations
@app.route('/create_vehicle_station', methods=['POST'])
@jwt_required()
def create_vehicle_station():
    data = request.get_json()
    insert_vehicle_station(data)
    return jsonify({"message":"Station Details Successfully Inserted"}, data)

#Assigning multiple vehicles to stations
@app.route('/inventory', methods=['POST'])
@jwt_required()
def inventory():
    data = request.get_json()
    assign_vehicle(data)
    return jsonify({"message":"Station Alloted with Cars List Successfully Inserted"}, data)

#Fetching the list of vehicles in particular station
@app.route('/retrieve_vehicles', methods=['GET'])
def retrieve_vehicles():
    data = request.get_json()
    vehicle_dict = vehicles_list(data)
    return(vehicle_dict)

#Ordering Vehicle
@app.route('/order_vehicle', methods=["POST"])
def order_vehicle():
    data = request.get_json()
    detail = place_order(data)
    return jsonify({"message":"Successful!!"}, detail)

#Returning Vehicle
@app.route('/return_vehicle', methods=['POST'])
def return_vehicle():
    data = request.get_json()
    detail = return_order(data)
    return jsonify({"message":"Successful!!"}, detail)

if __name__ =="__main__":
    app.run(debug=True)
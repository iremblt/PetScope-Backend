from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os 

app = Flask(__name__)

workingDirectory = os.getcwd()
configFile = os.path.join(workingDirectory, 'config.json')

with open(configFile, 'r') as jsonConfig:
    config = json.load(jsonConfig)

DATABASE_CONNECTION = config['DATABASE_CONNECTION']
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.app_context().push()

db = SQLAlchemy(app)

class Pets(db.Model):
    __tablename__ = 'Pets'
    pet_id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.Integer, nullable=False) #0 lost, 1 found
    date_time = db.Column(db.String(500), nullable=False) #convert to datetime
    pet_name = db.Column(db.String(500), nullable=False)
    pet_breed = db.Column(db.String(500), nullable=False)
    pet_color = db.Column(db.String(500), nullable=True)
    pet_age = db.Column(db.Integer, nullable=True)
    pet_gender = db.Column(db.String(10), nullable=True)
    pet_image = db.Column(db.String(5000), nullable=False)
    pet_gender = db.Column(db.String(10), nullable=True)
    pet_details = db.Column(db.String(5000), nullable = True)
    pet_lost_location = db.Column(db.String(5000), nullable = False)
    # created_id = db.Column(db.Integer,nullable = False)
    created_id = db.Column(db.Integer,db.ForeignKey('Users.user_id'))
    def __init__(__self__,record_type,date_time,pet_name,pet_breed,pet_color,pet_age,pet_gender,pet_image,pet_details,pet_lost_location,created_id):
        __self__.record_type = record_type
        __self__.date_time = date_time
        __self__.pet_name = pet_name
        __self__.pet_breed = pet_breed
        __self__.pet_color = pet_color
        __self__.pet_age = pet_age
        __self__.pet_gender = pet_gender
        __self__.pet_image = pet_image
        __self__.pet_details = pet_details
        __self__.pet_lost_location = pet_lost_location
        __self__.created_id = created_id

class Users(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    telophone_number = db.Column(db.String(50), nullable=True)
    user_type =  db.Column(db.Integer, nullable=False) # 0 found pet, 1 looking pet
    created_at = db.Column(db.String(500), nullable=False) #convert to datetime
    pets = db.relationship('Pets',backref='Users')
    def __init__(__self__,full_name,email,password,telophone_number,user_type,created_at):
        __self__.full_name = full_name
        __self__.email = email
        __self__.password = password
        __self__.telophone_number = telophone_number
        __self__.user_type = user_type
        __self__.created_at = created_at

class UserSession(db.Model):
    __tablename__ = 'UserSession'
    user_session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    login_date = db.Column(db.DateTime, nullable=False)
    expire_date = db.Column(db.DateTime, nullable=False)
    logged_out = db.Column(db.Boolean, nullable=False)
    jw_token = db.Column(db.String(4000), nullable=False)

    def __init__(__self__,user_id,login_date,expire_date,logged_out,jw_token):
        __self__.user_id = user_id
        __self__.login_date = login_date
        __self__.expire_date = expire_date
        __self__.logged_out = logged_out
        __self__.jw_token = jw_token

# class addressDetail(db.Model):
#     __tablename__ = 'addressDetail'
#     address_id = db.Column(db.Integer, primary_key=True)
#     location_name = db.Column(db.String(500), nullable=False)
#     zip = db.Column(db.Integer, nullable=False)
#     state = db.Column(db.String(250), nullable=False)
#     latitude = db.Column(db.Integer, nullable=False)
#     longitude =  db.Column(db.Integer, nullable=False)
#     def __init__(__self__,address_id,location_name,zip,state,latitude,longitude):
#         __self__.address_id = address_id
#         __self__.location_name = location_name
#         __self__.zip = zip
#         __self__.state = state
#         __self__.latitude = latitude
#         __self__.longitude = longitude



db.create_all()
db.session.commit()

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()
class Users(UserMixin,db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    telophone_number = db.Column(db.Integer, nullable=True)
    user_type =  db.Column(db.Integer, nullable=False) # 0 found pet, 1 looking pet
    created_at = db.Column(db.DateTime, nullable=False)
    pets = db.relationship('Pets',backref='users',lazy=True)

    def __init__(__self__,full_name,email,password,telophone_number,user_type,created_at):
        __self__.full_name = full_name
        __self__.email = email
        __self__.password = password
        __self__.telophone_number = telophone_number
        __self__.user_type = user_type
        __self__.created_at = created_at


class Pets(db.Model):
    __tablename__ = 'Pets'
    pet_id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.Integer, nullable=False) #0 lost, 1 found
    date_time = db.Column(db.DateTime, nullable=False)
    pet_name = db.Column(db.String(500), nullable=False)
    pet_breed = db.Column(db.String(500), nullable=False)
    pet_color = db.Column(db.String(500), nullable=True)
    pet_age = db.Column(db.Integer, nullable=True)
    pet_gender = db.Column(db.String(10), nullable=True)
    pet_image = db.Column(db.String(5000), nullable=True)
    pet_gender = db.Column(db.String(10), nullable=True)
    pet_details = db.Column(db.String(5000), nullable = True)
    pet_lost_location = db.Column(db.String(5000), nullable = True)
    created_id = db.Column(db.Integer,db.ForeignKey(Users.user_id))
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
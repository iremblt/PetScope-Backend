from flask_sqlalchemy import SQLAlchemy
from entities.pets import Pets


db = SQLAlchemy()
class Users(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    telophone_number = db.Column(db.Integer, nullable=True)
    user_type =  db.Column(db.Integer, nullable=False) # 0 found pet, 1 looking pet
    created_at = db.Column(db.DateTime, nullable=False)
    pets = db.relationship(Pets,backref='users')

    def __init__(__self__,full_name,email,password,telophone_number,user_type,created_at):
        __self__.full_name = full_name
        __self__.email = email
        __self__.password = password
        __self__.telophone_number = telophone_number
        __self__.user_type = user_type
        __self__.created_at = created_at
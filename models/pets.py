#Before

# import flask
# from flask_marshmallow import Marshmallow

# app = flask.Flask(__name__)

# marsh = Marshmallow(app)
# class petSchema(marsh.Schema):
#     class Meta:
#         fields = ('Animal ID','Intake Type','In Date','Pet name','Animal Type','Pet Age','Pet Size','Color','Breed','Sex','URL Link','Crossing')


#Afterrr

import flask
import json
import os 
from flask_marshmallow import Marshmallow

app = flask.Flask(__name__)

workingDirectory = os.getcwd()
configFile = os.path.join(workingDirectory, 'config.json')

with open(configFile, 'r') as jsonConfig:
    config = json.load(jsonConfig)

DATABASE_CONNECTION = config['DATABASE_CONNECTION']
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION

marsh = Marshmallow(app)
class PetsSchema(marsh.Schema):
    class Meta:
        fields = ('pet_id','record_type','date_time','pet_name','pet_breed','pet_color','pet_age','pet_gender','pet_image','pet_details','pet_lost_location','created_id')
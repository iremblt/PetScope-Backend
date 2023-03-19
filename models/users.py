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
class UsersSchema(marsh.Schema):
    class Meta:
        fields = ('user_id','full_name','email','password','telophone_number','user_type','created_at')
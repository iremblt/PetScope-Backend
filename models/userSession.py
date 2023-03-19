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
class UserSessionSchema(marsh.Schema):
        class Meta:
            fields = ('user_id','login_date','expire_date','logged_out','jw_token')
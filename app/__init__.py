from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os 
from flask_login import LoginManager
from app import config

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


lm = LoginManager()
lm.init_app(app)

db = SQLAlchemy(app)#create sqlalchemy db obj
from app import models
from app import config_data


models.dict_tables_name.update(models.make_regions_models(config_data.regions))

db.create_all()
from app import db_api
from app import views
from app import tasks
from app import forms
from app import parser
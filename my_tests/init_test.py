from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

from settings.constants import DB_URL
from core import db
from models.actor import Actor  
from models.movie import Movie


app = Flask(__name__, instance_relative_config=False)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
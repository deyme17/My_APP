from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from sqlalchemy import inspect

from settings.constants import DB_URL
from core import db
from models.actor import Actor  
from models.movie import Movie

data = {'name': 'Megan Wolf', 'gender': 'female', 'date_of_birth': dt.strptime('15.05.1986', '%d.%m.%Y').date()}

app = Flask(__name__, instance_relative_config=False)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    obj = Actor.create(**data)
    print(obj)
    print(obj.__dict__)
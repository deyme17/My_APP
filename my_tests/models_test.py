from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

from settings.constants import DB_URL, DATE_FORMAT
from core import db
from models.actor import Actor  
from models.movie import Movie


app = Flask(__name__, instance_relative_config=False)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data = {'name': 'Yemelianov Maxim', 'gender': 'male', 'date_of_birth': dt.strptime('03.11.2005', DATE_FORMAT).date()}

with app.app_context():
    db.create_all()
    obj = Actor(**data)
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)
    print(obj)
    print(obj.__dict__)
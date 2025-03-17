from datetime import datetime as dt

from core import db
from models.relations import association
from models.base import Model

class Actor(Model, db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(11))
    date_of_birth = db.Column(db.Date)

    movies = db.relationship('Movie', 
                            secondary=association,
                            backref=db.backref('cast', uselist=True), 
                            lazy='dynamic',
                            overlaps="movies,cast"
                            )

    def __repr__(self):
        return '<Actor {}>'.format(self.name)
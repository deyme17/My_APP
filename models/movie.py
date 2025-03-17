from datetime import datetime as dt

from core import db
from models.relations import association
from models.base import Model


class Movie(Model, db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(20))

    actors = db.relationship('Actor', 
                            secondary=association,
                            backref=db.backref('filmography', uselist=True), 
                            lazy='dynamic',
                            overlaps="cast,filmography"
                            )

    def __repr__(self):
        return '<Movie {}>'.format(self.name)
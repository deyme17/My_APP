from core import db
from sqlalchemy import Table, Column, Integer, ForeignKey

association = Table('association', db.metadata,
                    Column('actor_id', Integer, ForeignKey('actors.id'), primary_key = True),
                    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key = True)
                    )
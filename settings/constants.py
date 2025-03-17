import os

DB_URL = os.environ.get('DB_URL', None)
if DB_URL is None:   
    raise Exception('ERROR: No DB_URL')         
#print(DB_URL)                                                      

ACTOR_FIELDS = ['id', 'name', 'gender', 'date_of_birth']
MOVIE_FIELDS = ['id', 'name', 'year', 'genre']

DATE_FORMAT = '%d.%m.%Y'
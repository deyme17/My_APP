from flask import jsonify, make_response

from ast import literal_eval

from models.actor import Actor  
from models.movie import Movie
from settings.constants import MOVIE_FIELDS, DATE_FORMAT
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    try:
        all_movies = Movie.query.all()
        movies = []

        for movie in all_movies:
            act = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            movies.append(act)

        return make_response(jsonify(movies), 200) 
    
    except Exception as error:
        return make_response(jsonify(error=str(error)), 400)
    

def get_movie_by_id():
    """
    Get record by id
    """
    try:
        data = get_request_data()

        # validate data ---------------------------------------------------------------------
        # check if id specified
        if 'id' not in data:
            return make_response(jsonify(error='No id specified.'), 400)

        # check if id is int
        try:
            row_id = int(data['id'])
        except ValueError:
            return make_response(jsonify(error='Id must be an integer.'), 400)

        # check if movie exists
        obj = Movie.query.get(row_id)
        if not obj:
            error = f'Movie with such id {row_id} does not exist.'
            return make_response(jsonify(error=error), 400)
        # ------------------------------------------------------------------------------------

        movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(movie), 200)

    except Exception as error:
        return make_response(jsonify(error=str(error)), 500)

def add_movie():
    """
    Add new movie
    """
    try:
        data = get_request_data()

        # validate data ---------------------------------------------------------------------
        required_fields = [field for field in MOVIE_FIELDS if field != 'id']
        missing_fields = [field for field in required_fields if field not in data]

        # check if missing fields
        if missing_fields:
            return make_response(jsonify(error=f"Missing required fields: {', '.join(missing_fields)}."), 400)

        # check for invalid fields
        invalid_fields = [field for field in data if field not in MOVIE_FIELDS]
        if invalid_fields:
            return make_response(jsonify(error=f"Invalid fields: {', '.join(invalid_fields)}."), 400)

        # check if year is int
        try:
            data['year'] = int(data['year'])
        except ValueError:
            return make_response(jsonify(error='Year must be an integer.'), 400)
        # -------------------------------------------------------------------------------------

        new_record = Movie.create(**data)
        new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}

        return make_response(jsonify(new_movie), 200)

    except Exception as err:
        return make_response(jsonify(error=str(err)), 500)


def update_movie():
    """
    Update movie record by id
    """
    try:
        data = get_request_data()

        # validate data ---------------------------------------------------------------------
        # check if id specified
        if 'id' not in data:
            error = 'No id specified.'
            return make_response(jsonify(error=error), 400)

        # check if id is int
        try:
            row_id = int(data['id'])
        except ValueError:
            error = 'Id must be an integer.'
            return make_response(jsonify(error=error), 400)

        # check if movie exists
        obj = Movie.query.filter_by(id=row_id).first()
        if not obj:
            error = f'Movie with such id {row_id} does not exist.'
            return make_response(jsonify(error=error), 400)
        
        # check if missing fields
        invalid_fields = [field for field in data if field not in MOVIE_FIELDS]
        if invalid_fields:
            error = f"Missing required fields: {', '.join(invalid_fields)}."
            return make_response(jsonify(error=error), 400)

        if 'year' in data:
        # check if year is int
            try:
                year = int(data['year'])
            except ValueError:
                error = 'Year must be an integer.'
                return make_response(jsonify(error=error), 400)
        # -------------------------------------------------------------------------------------

        upd_record = Movie.update(row_id, **{k: v for k, v in data.items() if k != 'id'})
        upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}

        return make_response(jsonify(upd_movie), 200)

    except Exception as error:
        return make_response(jsonify(error=str(error)), 500)


def delete_movie():
    """
    Delete movie by id
    """
    try:
        data = get_request_data()

        # validate data ---------------------------------------------------------------------
        # check if id specified
        if 'id' not in data:
            error = 'No id specified.'
            return make_response(jsonify(error=error), 400)

        try:
            # check if id is int
            row_id = int(data['id'])
        except ValueError:
            error = 'Id must be an integer.'
            return make_response(jsonify(error=error), 400)
        
        # check if record exists
        obj = Movie.query.filter_by(id=row_id).first()
        if not obj:
            error = f'Movie with such id {row_id} does not exist.'
            return make_response(jsonify(error=error), 400)
        # -------------------------------------------------------------------------------------

        Movie.delete(row_id)
        massage = 'Record successfully deleted.'
        return make_response(jsonify(message=massage), 200)
    
    except Exception as error:
        return make_response(jsonify(error=str(error)), 400)
    
    
def movie_add_relation():
    """
    Add an actor to movie's cast
    """
    try:
        data = get_request_data()

        # validate data ---------------------------------------------------------------------
        # check if ids specified
        if 'id' not in data or data['id'] is None:
            error = 'No movie id specified.'
            return make_response(jsonify(error=error), 400)
        if 'relation_id' not in data or data['relation_id'] is None:
            error = 'No actor id specified.'
            return make_response(jsonify(error=error), 400)

        try:
            # check if ids are integers
            movie_id = int(data['id'])
            actor_id = int(data['relation_id'])
        except ValueError:
            error = 'Ids must be integers.'
            return make_response(jsonify(error=error), 400)
        
        # check if records exist
        movie = Movie.query.filter_by(id=movie_id).first()
        if not movie:
            error = f'Movie with such id {movie_id} does not exist.'
            return make_response(jsonify(error=error), 400)
        
        actor = Actor.query.filter_by(id=actor_id).first()
        if not actor:
            error = f'Actor with such id {actor_id} does not exist.'
            return make_response(jsonify(error=error), 400)
        # -------------------------------------------------------------------------------------

        movie = Movie.add_relation(movie_id, actor) 
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
    
    except Exception as error:
        return make_response(jsonify(error=str(error)), 500)


def movie_clear_relations():
    """
    Clear all relations by id
    """
    try:
        data = get_request_data()

        # validate data ---------------------------------------------------------------------
        # check if id specified
        if 'id' not in data:
            error = 'No movie id specified.'
            return make_response(jsonify(error=error), 400)

        try:
            # check if id is int
            row_id = int(data['id'])
        except ValueError:
            error = 'Id must be an integer.'
            return make_response(jsonify(error=error), 400)
        
        # check if record exists
        obj = Movie.query.filter_by(id=row_id).first()
        if not obj:
            error = f'Movie with such id {row_id} does not exist.'
            return make_response(jsonify(error=error), 400)
        # -------------------------------------------------------------------------------------

        movie = Movie.clear_relations(row_id)
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
    
    except Exception as error:
        return make_response(jsonify(error=str(error)), 400)
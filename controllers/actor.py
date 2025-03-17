from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor  
from models.movie import Movie
from settings.constants import ACTOR_FIELDS, DATE_FORMAT
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """  
    try:
        all_actors = Actor.query.all()
        actors = []

        for actor in all_actors:
            act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            actors.append(act)

        return make_response(jsonify(actors), 200) 
    
    except Exception as error:
        return make_response(jsonify(error=str(error)), 400)

  
def get_actor_by_id():
    """Get record by id"""
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

        # check record exists
        obj = Actor.query.get(row_id)
        if not obj:
            error = f'Actor with such id {row_id} does not exist.'
            return make_response(jsonify(error=error), 400)
        # ------------------------------------------------------------------------------------

        actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(actor), 200)

    except Exception as error:
        return make_response(jsonify(error=str(error)), 500)


def add_actor():
    """
    Add new actor
    """
    try:
        data = get_request_data()

        # validate data ---------------------------------------------------------------------
        required_fields = [field for field in ACTOR_FIELDS if field != 'id']
        missing_fields = [field for field in required_fields if field not in data]

        # check if missing fields
        if missing_fields:
            return make_response(jsonify(error=f"Missing required fields: {', '.join(missing_fields)}."), 400)

        # check for invalid fields
        invalid_fields = [field for field in data if field not in ACTOR_FIELDS]
        if invalid_fields:
            return make_response(jsonify(error=f"Invalid fields: {', '.join(invalid_fields)}."), 400)

        # check date format
        if 'date_of_birth' in data:
            try:
                data['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT).date()
            except ValueError:
                error = f"Date must be in format {DATE_FORMAT}."
                return make_response(jsonify(error=error), 400)
        # -------------------------------------------------------------------------------------

        new_record = Actor.create(**data)
        new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}

        return make_response(jsonify(new_actor), 200)

    except Exception as err:
        return make_response(jsonify(error=str(err)), 500)


def update_actor():
    """
    Update actor record by id
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

        # check if such actor exists
        obj = Actor.query.filter_by(id=row_id).first()
        if not obj:
            error = f'Actor with such id {row_id} does not exist.'
            return make_response(jsonify(error=error), 400)

        # check if missing fields
        invalid_fields = [field for field in data if field not in ACTOR_FIELDS]
        if invalid_fields:
            error = f"Missing required fields: {', '.join(invalid_fields)}."
            return make_response(jsonify(error=error), 400)

        # check date format
        if 'date_of_birth' in data:
            try:
                data['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT).date()
            except ValueError:
                error = f"Date must be in format {DATE_FORMAT}."
                return make_response(jsonify(error=error), 400)
        # -------------------------------------------------------------------------------------

        upd_record = Actor.update(row_id, **{k: v for k, v in data.items() if k != 'id'})
        upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}

        return make_response(jsonify(upd_actor), 200)

    except Exception as error:
        return make_response(jsonify(error=str(error)), 500)
    

def delete_actor():
    """
    Delete actor by id
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
        obj = Actor.query.filter_by(id=row_id).first()
        if not obj:
            error = f'Record with such id {row_id} does not exist.'
            return make_response(jsonify(error=error), 400)
        # -------------------------------------------------------------------------------------

        Actor.delete(row_id)
        massage = 'Record successfully deleted.'
        return make_response(jsonify(message=massage), 200)
    
    except Exception as error:
        return make_response(jsonify(error=str(error)), 400)


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    try:
        data = get_request_data()

        # validate data ---------------------------------------------------------------------
        # check if ids specified
        if 'id' not in data:
            error = 'No actor id specified.'
            return make_response(jsonify(error=error), 400)
        if 'relation_id' not in data or data['relation_id'] is None:
            error = 'No movie id specified.'
            return make_response(jsonify(error=error), 400)

        try:
            # check if ids is ints
            actor_id = int(data['id'])
            movie_id = int(data['relation_id'])
        except ValueError:
            error = 'Ids must be integers.'
            return make_response(jsonify(error=error), 400)
        
        # check if records exist
        actor = Actor.query.filter_by(id=actor_id).first()
        if not actor:
            error = f'Actor with such id {actor_id} does not exist.'
            return make_response(jsonify(error=error), 400)
        
        movie = Movie.query.filter_by(id=movie_id).first()
        if not movie:
            error = f'Movie with such id {movie_id} does not exist.'
            return make_response(jsonify(error=error), 400)
        # -------------------------------------------------------------------------------------

        actor = Actor.add_relation(actor_id, movie) 
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    
    except Exception as error:
        return make_response(jsonify(error=str(error)), 400)


def actor_clear_relations():
    """
    Clear all relations by id
    """
    try:
        data = get_request_data()

        # validate data ---------------------------------------------------------------------
        # check if id specified
        if 'id' not in data:
            error = 'No actor id specified.'
            return make_response(jsonify(error=error), 400)

        try:
            # check if id is int
            row_id = int(data['id'])
        except ValueError:
            error = 'Id must be an integer.'
            return make_response(jsonify(error=error), 400)
        
        # check if record exists
        obj = Actor.query.filter_by(id=row_id).first()
        if not obj:
            error = f'Actor with such id {row_id} does not exist.'
            return make_response(jsonify(error=error), 400)
        # -------------------------------------------------------------------------------------

        actor = Actor.clear_relations(row_id)
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    
    except Exception as error:
        return make_response(jsonify(error=str(error)), 400)
#!/usr/bin/python3
'''Contains the places view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_places(city_id=None, place_id=None):
    '''The method handler for the places endpoint.
    '''
    handlers = {
        'GET': get_places,
        'DELETE': remove_place,
        'POST': add_place,
        'PUT': update_place
    }
    if request.method in handlers:
        return handlers[request.method](city_id, place_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_places(city_id=None, place_id=None):
    '''Gets the place with the given id or all places in
    the city with the given id.
    '''
    if city_id:
        city = storage.get(City, city_id)
        if city:
            all_places = []
            if storage_t == 'db':
                all_places = list(city.places)
            else:
                all_places = list(filter(
                    lambda x: x.city_id == city_id,
                    storage.all(Place).values()
                ))
            places = list(map(lambda x: x.to_dict(), all_places))
            return jsonify(places)
    elif place_id:
        place = storage.get(Place, place_id)
        if place:
            return jsonify(place.to_dict())
    raise NotFound()


def remove_place(city_id=None, place_id=None):
    '''Removes a place with the given id.
    '''
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
    raise NotFound()


def add_place(city_id=None, place_id=None):
    '''Adds a new place.
    '''
    city = storage.get(City, city_id)
    if not city:
        raise NotFound()
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'user_id' not in data:
        raise BadRequest(description='Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        raise NotFound()
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


def update_place(city_id=None, place_id=None):
    '''Updates the place with the given id.
    '''
    xkeys = ('id', 'user_id', 'city_id', 'created_at', 'updated_at')
    place = storage.get(Place, place_id)
    if place:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        for key, value in data.items():
            if key not in xkeys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    raise NotFound()

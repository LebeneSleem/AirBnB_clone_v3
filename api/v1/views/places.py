#!/usr/bin/python3
'''Contains the places view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def handle_city_places(city_id):
    '''Retrieves the list of all Place objects of a City or creates a new Place.'''
    city = storage.get(City, city_id)
    if not city:
        raise NotFound()

    if request.method == 'GET':
        all_places = list(city.places)
        places = [place.to_dict() for place in all_places]
        return jsonify(places)

    elif request.method == 'POST':
        data = request.get_json()
        if not isinstance(data, dict):
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


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_place(place_id):
    '''Retrieves, deletes, or updates a Place object.'''
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound()

    if request.method == 'GET':
        return jsonify(place.to_dict())

    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if not isinstance(data, dict):
            raise BadRequest(description='Not a JSON')
        keys_to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in keys_to_ignore:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200

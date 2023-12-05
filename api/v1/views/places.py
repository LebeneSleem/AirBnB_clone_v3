#!/usr/bin/python3
'''Contains the places view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places_search', methods=['POST'])
def places_search():
    '''Retrieves all Place objects based on the JSON in the request body.'''
    try:
        data = request.get_json()
        if not data:
            raise BadRequest(description='Not a JSON')
    except Exception:
        raise BadRequest(description='Not a JSON')

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = []

    if not states and not cities and not amenities:
        # If no filters specified, retrieve all Place objects
        places = storage.all(Place).values()
    else:
        # Retrieve places based on the specified filters
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                places.extend(state.places)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

    # Filter places based on amenities
    if amenities:
        amenities_set = set(amenities)
        places = [place for place in places if amenities_set.issubset(
            amenity.id for amenity in place.amenities)]

    result = [place.to_dict() for place in set(places)]

    return jsonify(result)

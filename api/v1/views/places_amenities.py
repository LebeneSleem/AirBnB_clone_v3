#!/usr/bin/python3
'''Contains the places_amenities view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity

@app_views.route('/places/<place_id>/amenities', methods=['GET', 'DELETE', 'POST'])
@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE', 'POST'])
def handle_places_amenities(place_id=None, amenity_id=None):
    '''The method handler for the places_amenities endpoint.
    '''
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound()

    if request.method == 'GET':
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)

    elif request.method == 'DELETE' and amenity_id:
        return delete_amenity(place, amenity_id)

    elif request.method == 'POST' and amenity_id:
        return link_amenity(place, amenity_id)

    raise BadRequest()

def delete_amenity(place, amenity_id):
    '''Deletes an Amenity object from a Place.'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        raise NotFound()

    if storage_t == 'db':
        if amenity not in place.amenities:
            raise NotFound()

        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200

    elif storage_t == 'file':
        if amenity_id not in place.amenity_ids:
            raise NotFound()

        place.amenity_ids.remove(amenity_id)
        storage.save()
        return jsonify({}), 200

def link_amenity(place, amenity_id):
    '''Links an Amenity object to a Place.'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        raise NotFound()

    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    elif storage_t == 'file':
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200

        place.amenity_ids.append(amenity_id)
        storage.save()
        return jsonify(amenity.to_dict()), 201

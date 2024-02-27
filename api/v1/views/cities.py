#!/usr/bin/python3
""" Cities """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """ get cities """
    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    c = []
    for city in s.c:
        c.append(city.to_dict())
    return jsonify(c)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['GET'])
def get_city_id(city_id):
    """ get city by id """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete city"""
    c = storage.get("City", city_id)
    if c is None:
        abort(404)
    c.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """post city"""
    key = "State." + str(state_id)
    if key not in storage.all(State).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def put_city(city_id=None):
    """ put city """
    key = "City." + str(city_id)
    if key not in storage.all(City).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    for key, val in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200

#!/usr/bin/python3
""" states """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ get states """
    s = []
    for state in storage.all("State").values():
        s.append(state.to_dict())
    return jsonify(s)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """ get state with id"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    return jsonify(s.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete state"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    s.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """create state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    s = State(**request.get_json())
    s.save()
    return make_response(jsonify(s.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """put state"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for a, v in request.get_json().items():
        if a not in ['id', 'created_at', 'updated_at']:
            setattr(s, a, v)
    s.save()
    return jsonify(s.to_dict())

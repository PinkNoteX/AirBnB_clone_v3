#!/usr/bin/python3
""" states """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def get_states(state_id=None):
    """ get states """
    s = []
    key = "State." + str(state_id)
    if state_id is None:
        objs = storage.all(State)
        for key, value in objs.items():
            s.append(value.to_dict())
    elif key in storage.all(State).keys():
        return jsonify(storage.all(State)[key].to_dict())
    else:
        abort(404)
    return jsonify(s)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """delete state"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    s.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """create state"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    s = State(**request.get_json())
    s.save()
    return jsonify(s.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id=None):
    """put state"""
    k = "State." + str(state_id)
    if k not in storage.all(State).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    for key, val in request.get_json().items():
        if key not in ["created_at", "updated_at", "id"]:
            setattr(s, key, val)
    s.save()
    return jsonify(s.to_dict()), 200

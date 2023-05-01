#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API
actions
"""

from api.v1.views import app_views
from models.user import User
from flask import jsonify, abort, request
from models import storage

cls = User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
@app_views.route("/users/<string:user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id=None):
    """Retrieves a User object"""
    if user_id is not None:
        obj = storage.get(cls, user_id)
        if obj is not None:
            return jsonify(obj.to_dict())
        else:
            abort(404)
    else:
        objs = storage.all(cls)
        my_lst = []
        for obj in objs.values():
            my_lst.append(obj.to_dict())
        return jsonify(my_lst)


@app_views.route("/users/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deletes a User object"""
    obj = storage.get(cls, user_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        storage.reload()
        return jsonify({})


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a User"""
    my_dict = request.get_json(silent=True)
    if my_dict is None:
        abort(400, "Not a JSON")
    if "email" not in my_dict:
        abort(400, "Missing email")
    if "password" not in my_dict:
        abort(400, "Missing password")
    emails = my_dict["email"]
    passwords = my_dict['password']
    obj = cls(email=emails, password=passwords)
    storage.new(obj)
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 201


@app_views.route("/users/<string:user_id>", methods=["PUT"])
def update_user(user_id):
    """Updates a User object"""
    obj = storage.get(cls, user_id)
    if obj is None:
        abort(404)
    my_dict = request.get_json(silent=True)
    if my_dict is None:
        abort(400, "Not a JSON")
    for k, v in my_dict.items():
        if k == 'email':
            continue
        if k == 'id' or k == 'created_at' or k == 'updated_at':
            continue
        setattr(obj, k, v)
    obj.save()
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 200

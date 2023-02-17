from flask import Blueprint, request, jsonify, redirect, url_for

from ..controller import users_controller, companies_controller
from ..models.models import User, Company

api_scope = Blueprint("api", __name__)

@api_scope.route('/users', methods=['GET'])
def get_list():
    users_list = users_controller.lists()

    users_dict = [user._asdict() for user in users_list]

    return jsonify(users_dict)


@api_scope.route('/users/<id_>', methods=['GET'])
def get_details(id_):
    user = User(id=id_)

    user_new = users_controller.details(user)

    return jsonify(user_new._asdict())


@api_scope.route('/users', methods=['POST'])
def create():
    data = request.form
    print(data)
    user = User(first_name=data["firstName"], last_name=data["lastName"], email=data["email"])

    users_controller.create(user)

    return redirect(url_for('views.home'))


@api_scope.route('/users/<id_>', methods=['PUT'])
def update(id_):
    data = request.data

    user = User(id=id_, first_name=data["firstName"], last_name=data["lastName"], email=data["email"])

    user_new = users_controller.update(user)

    return jsonify(user_new._asdict())


@api_scope.route('/users/<id_>', methods=['DELETE'])
def delete(id_):
    user = User(id=id_)

    user_new = users_controller.delete(user)

    return jsonify(user_new._asdict())
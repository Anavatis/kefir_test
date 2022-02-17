import json

from flask import Blueprint, request, jsonify

from app.auth.authorize import auth_required
from app.error.schemas import ErrorResponseModel
from app.user.get import get_users_and_meta
from app.user.update import update_user

user_module = Blueprint("user_module", __name__)


@user_module.route('/users/current')
@auth_required
def get_current_user(user):
    response = jsonify(user.get_private_data())
    response.status_code = 200
    return response


@user_module.route('/users')
@auth_required
def get_users_list(user):
    page = request.args.get("page")
    size = request.args.get("size")
    response = jsonify(get_users_and_meta(page, size))
    response.status_code = 200

    return response


@user_module.route('/users/<pk>', methods=["PATCH"])
@auth_required
def update_user_data(user, pk):
    if int(pk) != user.id_:
        raise ErrorResponseModel(400, "Not access")

    patch_data = request.json
    user = update_user(user, **patch_data)

    response_data = user.get_private_data()
    response_data['id'] = user.id_
    response = jsonify(response_data)
    response.status_code = 200

    return response

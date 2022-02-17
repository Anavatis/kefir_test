from flask import Blueprint, request, jsonify, make_response

from app.admin.create import check_required_params_for_create, create_new_user
from app.admin.delete import delete_user_by_id
from app.admin.get import get_users_and_meta, get_user_private_data, get_user_by_id
from app.auth.authorize import admin_required
from app.error.schemas import ErrorResponseModel
from app.user.update import update_user_by_dict, check_params_access, private_access_params

admin = Blueprint("admin", __name__)


@admin.route('/private/users', methods=["GET"])
@admin_required
def get_users(admin_user):
    page = request.args.get("page")
    size = request.args.get("size")

    response = jsonify(get_users_and_meta(page, size))
    response.status_code = 200

    return response


@admin.route('/private/users', methods=["POST"])
@admin_required
def create_user(admin_user):
    check_required_params_for_create(request.json)
    user = create_new_user(request.json)

    response = jsonify(get_user_private_data(user))
    response.status_code = 200

    return response


@admin.route('/private/users/<pk>', methods=["GET"])
@admin_required
def get_user_data(admin_user, pk):
    user = get_user_by_id(pk)
    response = jsonify(get_user_private_data(user))
    response.status_code = 200

    return response


@admin.route('/private/users/<pk>', methods=['DELETE'])
@admin_required
def delete_user(admin_user, pk):
    delete_user_by_id(pk)

    response = make_response()
    response.status_code = 204
    return response


@admin.route('/private/users/<pk>', methods=['PATCH'])
@admin_required
def update_user(admin_user, pk):

    update_data = request.json
    if "id" not in update_data:
        raise ErrorResponseModel(400, "Bad Request")

    check_params_access(update_data, private_access_params)
    user = get_user_by_id(update_data.pop("id"))
    user = update_user_by_dict(user, update_data)

    response = jsonify(get_user_private_data(user))
    response.status_code = 200

    return response



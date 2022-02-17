from flask import Blueprint, request, jsonify

from app.auth import authorize
from app.auth.authorize import auth_required
from app.error.schemas import ErrorResponseModel

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["POST"])
def login():
    user_login = request.json.get("login")
    user_password = request.json.get("password")

    if not (user_login or user_password):
        raise ErrorResponseModel(400, "Missing login or password")

    user = authorize.authorize_user(user_login, user_password)

    response = jsonify(user.get_private_data())
    response.set_cookie("login", user.login)
    response.set_cookie("access", user.cookie_token)
    response.status_code = 200

    return response


@auth.route('/logout', methods=["GET"])
def logout():
    response = jsonify()
    response.set_cookie("login", "", 0)
    response.set_cookie("access", "", 0)
    response.status_code = 200
    return response

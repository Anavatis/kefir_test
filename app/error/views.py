from flask import Blueprint, jsonify

from app.error.schemas import ErrorResponseModel, HTTPValidationError, UnauthorizedUserError

error = Blueprint("error", __name__)


@error.app_errorhandler(ErrorResponseModel)
def handle_response_error(e):
    response = jsonify({"error": e.to_dict()})
    response.status_code = e.code
    return response


@error.app_errorhandler(HTTPValidationError)
def handler_http_validation_error(e):
    response = jsonify({"error": e.to_dict()})
    response.status_code = e.code
    return response


@error.app_errorhandler(UnauthorizedUserError)
def handler_unauth_error(e):
    response = jsonify({"error": e.to_dict()})
    response.status_code = e.code
    return response


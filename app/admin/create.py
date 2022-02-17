from app import db
from app.error.schemas import ErrorResponseModel
from app.user.models import User


def check_required_params_for_create(json):
    required_params = ["first_name", "last_name", "email",
                       "is_admin", "password"]

    if list(filter(lambda x: x not in json, required_params)):
        raise ErrorResponseModel(400, "Bad Request")


def create_new_user(params):

    password = params.pop('password')
    user = User(**params)
    user.password = password

    db.session.add(user)
    db.session.commit()

    return user

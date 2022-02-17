import functools

from flask import request

from app import db
from app.error.schemas import HTTPValidationError, ValidationError, UnauthorizedUserError, ErrorResponseModel
from app.extensions import pwd_context
from app.utils import save_to_db
from models.user import User
import secrets


def authorize_user(login: str, password: str) -> User:
    user = db.session.query(User).filter_by(login=login).first()
    check_valid_auth(user, password)

    cookie_token = create_cookie_token()
    user.cookie_token = cookie_token

    save_to_db(user)
    return user


def check_valid_auth(user: User, password: str):
    if user is None or not pwd_context.verify(password, user.password):
        raise HTTPValidationError(ValidationError(
            msg="Incorrect auth data",
            type_="incorrect_auth"
        ))


def autorize_user_by_cookie(login: str, access_token: str) -> User:
    user = db.session.query(User).filter_by(login=login).first()
    if user is None or not user.cookie_token or not user.cookie_token == access_token:
        raise UnauthorizedUserError
    return user


def create_cookie_token() -> str:
    token = secrets.token_hex()
    return token


def get_auth_cookies_or_error():
    login = request.cookies.get("login")
    access_token = request.cookies.get("access")

    if not (login or access_token):
        raise UnauthorizedUserError

    return login, access_token


def auth_required(f):

    @functools.wraps(f)
    def decorator(*args, **kwargs):

        login, access_token = get_auth_cookies_or_error()
        user = autorize_user_by_cookie(login, access_token)

        return f(user, *args, **kwargs)

    return decorator


def admin_required(f):

    @functools.wraps(f)
    def decorator(*args, **kwargs):

        login, access_token = get_auth_cookies_or_error()
        user = autorize_user_by_cookie(login, access_token)

        if not user.is_admin:
            ErrorResponseModel(403, "no access for this action")

        return f(user, *args, **kwargs)

    return decorator



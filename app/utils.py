from flask import Response

from app import db
from app.error.schemas import ErrorResponseModel


def check_int_values_correct(*args):

    updated_values = []
    try:
        for v in args:
            updated_values.append(int(v))
    except Exception:
        raise ErrorResponseModel(400, "Bad request")

    return updated_values


def save_to_db(*instances):
    for i in instances:
        db.session.add(i)
    db.session.commit()

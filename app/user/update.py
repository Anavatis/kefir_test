from app import db
from app.error.schemas import ErrorResponseModel


default_access_params = ["first_name", "last_name", "other_name",
                     "email", "phone", "birthday"]
private_access_params = default_access_params + ["id", "city", "additional_info",
                                                 "is_admin"]


def update_user(user, **kwargs):
    check_params_access(kwargs)
    user = update_user_by_dict(user, kwargs)

    return user


def update_user_by_dict(user, params):
    for k, v in params.items():
        setattr(user, k, v)

    db.session.add(user)
    db.session.commit()

    return user


def check_params_access(params, access_params=None):
    if access_params is None: access_params = default_access_params
    print(params)
    if list(filter(lambda x: x not in access_params, params.keys())):
        raise ErrorResponseModel(400, "non-access params")

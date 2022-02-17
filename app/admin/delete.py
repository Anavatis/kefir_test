from app import db
from app.admin.get import get_user_by_id
from app.error.schemas import ErrorResponseModel


def delete_user_by_id(user_id):
    user = get_user_by_id(user_id)

    if not user:
        raise ErrorResponseModel(400, "User not exist")

    db.session.delete(user)
    db.session.commit()

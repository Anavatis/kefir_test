from app import db
from app.error.schemas import ErrorResponseModel
from app.user.models import User
from app.user.utils import check_int_values_correct


def get_users_and_meta(page=0, size=10):
    query = get_query_by_page_and_size(page, size)

    users = [x.get_public_data() for x in query.all()]
    if not users: raise ErrorResponseModel(400, "Page not found")

    meta = {"total": query.count(),
            "page": page,
            "size": len(users)}

    return {"data": users,
            "meta": {"pagination": meta}}


def get_query_by_page_and_size(page, size):

    page, size = check_int_values_correct(page, size)
    query = db.session.query(User)
    query = query.limit(size)
    query = query.offset(page * size)

    return query



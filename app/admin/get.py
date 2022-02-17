from app import db
from app.error.schemas import ErrorResponseModel
from app.user.get import get_query_by_page_and_size
from app.user.models import User


def get_users_and_meta(page, size):
    query = get_query_by_page_and_size(page, size)

    users = query.all()
    users_data = [x.get_public_data() for x in users]
    if not users_data: raise ErrorResponseModel(400, "Page not found")

    meta_data = get_meta_data(query, page, users_data, users)

    return {"data": users_data,
            "meta": meta_data}


def get_meta_data(query, page, users_data, users):

    paginate_meta = {"total": query.count(),
                     "page": page,
                     "size": len(users_data)}
    cities = set([x.city for x in users if x.city])
    hint_meta = [[x.id_, x.city_name] for x in cities]
    meta_data = {"pagination": paginate_meta,
                 "hint_meta": hint_meta}

    return meta_data


def get_user_by_id(user_id):
    return db.session.query(User).get(user_id)


def get_user_private_data(user: User) -> dict:
    user_dict = user.get_private_data()
    city_name = "" if not user.city else user.city.city_name
    user_dict.update({
        "id": user.id_,
        "city": city_name,
        "additional_info": user.additional_info
    })

    return user_dict

from typing import List

from .connection import _fetch_all, _fetch_lastrow_id, _fetch_none, _fetch_one
#from ..models.models import Favorite
#from ..models.exceptions import FavoriteAlreadyExists, FavoriteNotFound

from faker import Faker


def create(favorite: Favorite) -> Favorite:
    query = """INSERT INTO favorites VALUES (:id_user, :id_company)"""

    favorite_dict = favorite._asdict()

    #id_ = _fetch_lastrow_id(query, favorite_dict)

    #favorite_dict["id"] = id_
    return Favorite(**favorite_dict)


def delete(favorite: Favorite) -> Favorite:
    query = "DELETE FROM favorites WHERE  id_user= ? and id_company= ?"
    parameters = [favorite.id_user,favorite.id_company]

    _fetch_none(query, parameters)

    return favorite


def list_all() -> List[Favorite]:
    query = "SELECT  * FROM favorites"
    records = _fetch_all(query)

    favorites = []
    for record in records:
        favorite = Favorite(id_user=record[0], id_company=record[1])
        favorites.append(favorite)

    return favorites
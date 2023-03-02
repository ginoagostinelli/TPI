from typing import List

from .connection import _fetch_all, _fetch_lastrow_id, _fetch_none, _fetch_one
from ..models.models import Favorite
#from ..models.exceptions import FavoriteAlreadyExists, FavoriteNotFound

from faker import Faker


def create(favorite: Favorite) -> Favorite:
    query = "INSERT INTO favorite VALUES (:id_user, :id_company)"

    favorite_params = [favorite.id_user,favorite.id_company]

    #id_ = _fetch_lastrow_id(query, favorite_dict)

    #favorite_dict["id"] = id_
    _fetch_none(query, favorite_params)
    return favorite




def delete(favorite: Favorite) -> Favorite:
    query = "DELETE FROM favorite WHERE  id_user= ? and id_company= ?"
    parameters = [favorite.id_user,favorite.id_company]

    _fetch_none(query, parameters)

    return favorite


def list_all() -> List[Favorite]:
    query = "SELECT  * FROM favorite"
    records = _fetch_all(query)

    favorites = []
    for record in records:
        favorite = Favorite(id_user=record[0], id_company=record[1])
        favorites.append(favorite)

    return favorites


def list(id_user:int) -> List[str]:
    query = "SELECT id_company FROM favorite where id_user= ?"
    parameters = [id_user]
    records = _fetch_all(query,parameters)
    
    favorites = []
    for record in records:
        id_company=record[0]
        favorites.append(id_company)

    return favorites

def exists(fav:Favorite) -> List[str]:
    query = "SELECT id_company FROM favorite where id_user= ? and id_company= ?"
    parameters = [fav.id_user,fav.id_company]
    records = _fetch_all(query,parameters)

    favorites = []
    for record in records:
        id_company=record[0]
        favorites.append(id_company)

    return favorites
from typing import List

from ..database import user_db
from ..models.models import User
from ..helpers import helper


def create(user_: User) -> User:
    user = helper.format_name(user_)
    helper.validate_user(user)
    return user_db.create(user)


def update(user: User) -> User:
    user = helper.format_name(user)
    helper.validate_user(user)
    return user_db.update(user)


def delete(user: User) -> User:
    return user_db.delete(user)


def lists() -> List[User]:
    return user_db.list_all()


def details(user: User) -> User:
    return user_db.detail(user)
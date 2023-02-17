from typing import List

from .connection import _fetch_all, _fetch_lastrow_id, _fetch_none, _fetch_one
from ..models.models import User
from ..models.exceptions import UserAlreadyExists, UserNotFound

from faker import Faker


def create(user: User) -> User:
    if user_exists("email", user.email):
        raise UserAlreadyExists(f"Email {user.email} is already used")

    query = """INSERT INTO users VALUES (:first_name, :last_name, :email)"""

    user_dict = user._asdict()

    id_ = _fetch_lastrow_id(query, user_dict)

    user_dict["id"] = id_
    return User(**user_dict)


def update(user: User) -> User:
    if not user_exists("oid", user.id):
        raise UserNotFound("User not Found!")

    query = """UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email
               WHERE oid = :oid"""

    parameters = user._asdict()

    _fetch_none(query, parameters)

    return user


def delete(user: User) -> User:
    if not user_exists("oid", user.id):
        raise UserNotFound("User not Found!")

    query = "DELETE FROM users WHERE oid = ?"
    parameters = [user.id]

    _fetch_none(query, parameters)

    return user


def list_all() -> List[User]:
    query = "SELECT oid, * FROM users"
    records = _fetch_all(query)

    users = []
    for record in records:
        user = User(id=record[0], first_name=record[1], last_name=record[2], email=record[3])
        users.append(user)

    return users


def detail(user: User) -> User:
    query = "SELECT oid, * FROM users WHERE oid=?"
    parameters = [user.id]

    record = _fetch_one(query, parameters)

    if record is None:
        raise UserNotFound(f"No user with id: {user.id}")

    user = User(id=record[0], first_name=record[1], last_name=record[2], email=record[3])

    return user


def user_exists(field: str, value: str) -> bool:
    query = f"SELECT oid, email FROM users WHERE {field}=?"
    parameters = [value]

    record = _fetch_one(query, parameters)

    return bool(record)


def reset_table() -> None:
    query = "DROP TABLE IF EXISTS users"
    _fetch_none(query)

    fields = """(first_name text, last_name text, email text)"""
    query = f"CREATE TABLE IF NOT EXISTS users {fields}"

    _fetch_none(query)

    fake = Faker()
    fake.seed_instance(42)

    for _ in range(10):
        test_user = User(first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            email=fake.email())

        create(test_user)
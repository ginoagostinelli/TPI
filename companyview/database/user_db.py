from typing import List

from .connection import _fetch_all, _fetch_lastrow_id, _fetch_none, _fetch_one
from ..models.models import User
from ..models.exceptions import UserAlreadyExists, UserNotFound

from faker import Faker


def create(user: User) -> User:
    if user_exists("email", user.email):
        raise UserAlreadyExists(f"Email {user.email} is already used")

    query = """INSERT INTO user VALUES (:id, :name , :email, :password)"""

    user_dict = [None,user.name,user.email,user.password]
    
    id_ = _fetch_lastrow_id(query,user_dict)

    user.id = id_
    return user


def update(user: User) -> User:
    if not user_exists("oid", user.id):
        raise UserNotFound("User not Found!")

    query = """UPDATE user SET first_name = :first_name, last_name = :last_name, email = :email
               WHERE oid = :oid"""

    parameters = user._asdict()

    _fetch_none(query, parameters)

    return user


def delete(user: User) -> User:
    if not user_exists("oid", user.id):
        raise UserNotFound("User not Found!")

    query = "DELETE FROM user WHERE oid = ?"
    parameters = [user.id]

    _fetch_none(query, parameters)

    return user


def list_all() -> List[User]:
    query = "SELECT oid, * FROM user"
    records = _fetch_all(query)

    user = []
    for record in records:
        user = User(id=record[0], first_name=record[1], last_name=record[2], email=record[3])
        user.append(user)

    return user


def detail(user: User) -> User:
    query = "SELECT oid, * FROM user WHERE oid=?"
    parameters = [user.id]

    record = _fetch_one(query, parameters)

    if record is None:
        raise UserNotFound(f"No user with id: {user.id}")

    user = User(name=record[1], email=record[2],id=record[0], password=record[3])

    return user

def get_by_email(email) -> User:
    query = "SELECT * FROM user WHERE email=?"
    parameters = [email]

    record = _fetch_one(query, parameters)

    if record is None:
        return None
        #raise UserNotFound(f"No user with mail: {email}")

    user = User(name=record[1], email=record[2],id=record[0], password=record[3])

    return user

def get_by_id(id) -> User:
    query = "SELECT * FROM user WHERE id=?"
    parameters = [id]

    record = _fetch_one(query, parameters)

    if record is None:
        return None
        #raise UserNotFound(f"No user with mail: {user.email}")

    user = User(id=record[0], name=record[1], email=record[2], password=record[3])

    return user


def user_exists(field: str, value: str) -> bool:
    query = f"SELECT oid, email FROM user WHERE {field}=?"
    parameters = [value]

    record = _fetch_one(query, parameters)

    return bool(record)


def reset_table() -> None:
    query = "DROP TABLE IF EXISTS user"
    _fetch_none(query)

    fields = """(first_name text, last_name text, email text)"""
    query = f"CREATE TABLE IF NOT EXISTS user {fields}"

    _fetch_none(query)

    fake = Faker()
    fake.seed_instance(42)

    for _ in range(10):
        test_user = User(first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            email=fake.email())

        create(test_user)



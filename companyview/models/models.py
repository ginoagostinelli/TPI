from typing import NamedTuple, Optional
from pandas import DataFrame
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Company(NamedTuple):
    id: Optional[int] = None
    name: Optional[str] = None
    ticker: Optional[str] = None
    stock: Optional[DataFrame] = None
    news: Optional[dict] = {}
    country: Optional[str] = None
    city: Optional[str] = None
    industry: Optional[str] = None
    employees: Optional[str] = None
    business: Optional[str] = None


class Favorite(NamedTuple):
    id_user: Optional[int] = None
    id_company: Optional[str] = None




class User(UserMixin):
    def __init__(self, name, email,id=None,password=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def __repr__(self):
        return '<User {}>'.format(self.email)

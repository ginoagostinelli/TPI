import re

from ..models.models import User
from ..models.exceptions import UserNotValid, CompanyNotValid


def validate_ticker(ticker: str) -> None:
    if ticker is None or len(ticker) == 0 or any(chr.isdigit() for chr in ticker):
        raise CompanyNotValid("The company name is incorrect")


def validate_user(user: User) -> None:
    if not __email_is_valid(user.email):
        raise UserNotValid(f"The email address: {user.email} is not valid")

    if None in (user.first_name, user.last_name, user.email):
        raise UserNotValid("The user has no first name, last name or email")


def format_name(user: User) -> User:
    user_dict = user._asdict()
    user_dict["first_name"] = user.first_name.capitalize()
    user_dict["last_name"] = user.first_name.capitalize()

    return User(**user_dict)


def __email_is_valid(email: str) -> bool:
    if not isinstance(email, str):
        return False

    regex = r"^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$"

    return bool(re.search(regex, email))

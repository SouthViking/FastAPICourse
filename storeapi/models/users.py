from typing import Union

from pydantic import BaseModel


class User(BaseModel):
    id: Union[int, None] = None
    email: str


class UserIn(User):
    password: str

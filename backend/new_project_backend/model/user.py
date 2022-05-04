from typing import Optional

from pydantic import BaseModel


class UserNoPassword(BaseModel):
    user_id: int
    name: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    @classmethod
    def from_user(cls, user: 'User'):
        return UserNoPassword(**user.dict(exclude={'hashed_password'}))


class User(UserNoPassword):
    hashed_password: str


class AddingUser(BaseModel):
    name: str
    password: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

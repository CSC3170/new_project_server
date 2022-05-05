from typing import Optional

from pydantic import BaseModel


class UserNoPassword(BaseModel):
    user_id: int
    name: str
    is_admin: bool
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    @classmethod
    def from_user(cls, user: 'User'):
        return cls(**user.dict(exclude={'hashed_password'}))


class User(UserNoPassword):
    hashed_password: str


class AddingUser(BaseModel):
    name: str
    password: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class EditingUser(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

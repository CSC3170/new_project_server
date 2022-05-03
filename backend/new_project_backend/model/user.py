from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    hashed_password: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

from typing import Optional

from pydantic import BaseModel


class Book(BaseModel):
    book_id: int
    name: str
    description: Optional[str] = None
    words_count: int = 0


class AddingBook(BaseModel):
    name: str
    description: Optional[str] = None


class EditingBook(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

from typing import Optional

from pydantic import BaseModel


class Book(BaseModel):
    book_id: int
    name: str
    description: Optional[str] = None
    word_count: int


class AddingBook(BaseModel):
    name: str
    description: Optional[str] = None
    word_count: int


class EditingBook(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    word_count: Optional[int] = None

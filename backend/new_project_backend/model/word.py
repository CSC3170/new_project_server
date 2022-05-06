from typing import Optional

from pydantic import BaseModel


class Word(BaseModel):
    book_id: int
    word_id: int
    spelling: str
    translation: Optional[str] = None


class AddingWord(BaseModel):
    spelling: str
    translation: Optional[str] = None


class EditingWord(BaseModel):
    spelling: Optional[str] = None
    translation: Optional[str] = None

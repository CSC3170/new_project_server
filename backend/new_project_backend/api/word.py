from fastapi import APIRouter, Depends, HTTPException, status

from ..db.errors import DuplicateRecordError, NotExistsError
from ..db.word import word_db
from ..model.user import User
from ..model.word import AddingWord, EditingWord
from .auth import get_current_user, get_current_user_and_require_admin

word_router = APIRouter()


@word_router.get('/words/{book_name}')
async def query_words(book_name: str, user: User = Depends(get_current_user)):
    try:
        words = await word_db.query_by_book_name(book_name)
        return words
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Incorrect {error.name}',
        ) from error


@word_router.post('/word/{book_name}')
async def add_word(book_name: str, adding_word: AddingWord, user: User = Depends(get_current_user_and_require_admin)):
    try:
        word = await word_db.insert_by_book_name(book_name, adding_word)
        return word
    except DuplicateRecordError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Duplicate records',
        ) from error
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Incorrect {error.name}',
        ) from error


@word_router.patch('/word/{book_name}/{word_id}')
async def edit_word(
    book_name: str, word_id: int, editing_word: EditingWord, user: User = Depends(get_current_user_and_require_admin)
):
    try:
        word = await word_db.update_by_book_name_and_word_id(book_name, word_id, editing_word)
        return word
    except DuplicateRecordError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Duplicate records',
        ) from error
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Incorrect {error.name}',
        ) from error


@word_router.delete('/word/{book_name}/{word_id}')
async def delete_word(book_name: str, word_id: int, user: User = Depends(get_current_user_and_require_admin)):
    try:
        word = await word_db.delete_by_book_name_and_word_id(book_name, word_id)
        return word
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Incorrect {error.name}',
        ) from error

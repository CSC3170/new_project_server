from fastapi import APIRouter, Depends, HTTPException, status

from ..db.base import DuplicateRecordError, NotExistsError
from ..db.book import book_db
from ..model.book import AddingBook, EditingBook
from ..model.user import User
from .auth import get_current_user, get_current_user_and_require_admin

book_router = APIRouter()


@book_router.get('/books')
async def query_books(user: User = Depends(get_current_user)):
    books = await book_db.query()
    return books


@book_router.get('/book/{name}')
async def query_book(name: str, user: User = Depends(get_current_user)):
    try:
        book = await book_db.query_by_name(name)
        return book
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Incorrect book',
        ) from error


@book_router.post('/book')
async def add_book(adding_book: AddingBook, user: User = Depends(get_current_user_and_require_admin)):
    try:
        book = await book_db.insert(adding_book)
        return book
    except DuplicateRecordError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Duplicate records',
        ) from error


@book_router.patch('/book/{name}')
async def edit_book(name: str, editing_book: EditingBook, user: User = Depends(get_current_user_and_require_admin)):
    try:
        new_book = await book_db.update_by_name(name, editing_book)
        return new_book
    except DuplicateRecordError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Duplicate records',
        ) from error
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Incorrect book',
        ) from error


@book_router.delete('/book/{name}')
async def delete_book(name: str, user: User = Depends(get_current_user_and_require_admin)):
    try:
        new_book = await book_db.delete_by_name(name)
        return new_book
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Incorrect book',
        ) from error

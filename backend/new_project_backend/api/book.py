from fastapi import APIRouter, Depends, HTTPException, status

from ..db.book import book_db
from ..db.errors import DuplicateRecordError, NotExistsError
from ..model.book import AddingBook, EditingBook
from ..model.user import User
from .auth import get_current_user, get_current_user_and_require_admin

book_router = APIRouter()


@book_router.get('/books')
async def query_books(_: User = Depends(get_current_user)):
    books = await book_db.query()
    return books


@book_router.get('/book/{book_name}')
async def query_book(book_name: str, _: User = Depends(get_current_user)):
    try:
        book = await book_db.query_by_name(book_name)
        return book
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Incorrect {error.name}',
        ) from error


@book_router.get('/book-by-id/{book_id}')
async def query_book_by_id(book_id: int, _: User = Depends(get_current_user)):
    try:
        book = await book_db.query_by_book_id(book_id)
        return book
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Incorrect {error.name}',
        ) from error


@book_router.post('/book')
async def add_book(adding_book: AddingBook, _: User = Depends(get_current_user_and_require_admin)):
    try:
        book = await book_db.insert(adding_book)
        return book
    except DuplicateRecordError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Duplicate records',
        ) from error


@book_router.patch('/book/{book_name}')
async def edit_book(book_name: str, editing_book: EditingBook, _: User = Depends(get_current_user_and_require_admin)):
    try:
        book = await book_db.update_by_name(book_name, editing_book)
        return book
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


@book_router.delete('/book/{book_name}')
async def delete_book(book_name: str, _: User = Depends(get_current_user_and_require_admin)):
    try:
        book = await book_db.delete_by_name(book_name)
        return book
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Incorrect {error.name}',
        ) from error

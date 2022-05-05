from fastapi import APIRouter, Depends, HTTPException, status

from ..db.user import DuplicateRecordError, UserNotExistsError, user_db
from ..model.user import AddingUser, EditingUser, UserNoPassword
from .auth import get_current_user

user_router = APIRouter()


@user_router.get('/user')
async def query_user(user: UserNoPassword = Depends(get_current_user)):
    return UserNoPassword.from_user(user)


@user_router.post('/user/add')
async def add_user(adding_user: AddingUser):
    try:
        user = await user_db.insert(adding_user)
        return UserNoPassword.from_user(user)
    except DuplicateRecordError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Duplicate records',
        ) from error


@user_router.post('/user/edit')
async def edit_user(editing_user: EditingUser, user: UserNoPassword = Depends(get_current_user)):
    try:
        new_user = await user_db.update(user.user_id, editing_user)
        return UserNoPassword.from_user(new_user)
    except DuplicateRecordError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Duplicate records',
        ) from error
    except UserNotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Incorrect user',
        ) from error


@user_router.post('/user/delete')
async def delete_user(user: UserNoPassword = Depends(get_current_user)):
    try:
        new_user = await user_db.delete(user.user_id)
        return UserNoPassword.from_user(new_user)
    except UserNotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Incorrect user',
        ) from error

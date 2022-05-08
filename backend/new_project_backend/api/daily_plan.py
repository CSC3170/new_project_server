from fastapi import APIRouter, Depends, HTTPException, status

from ..db.daily_plan import daily_plan_db
from ..db.errors import DuplicateRecordError, NotExistsError
from ..db.word import word_db
from ..model.daily_plan import AddingDailyPlan, EditingDailyPlan
from ..model.user import User
from ..model.word import WordResponce
from .auth import get_current_user

daily_plan_router = APIRouter()


@daily_plan_router.get('/daily-plans')
async def query_daily_plans(user: User = Depends(get_current_user)):
    daily_plans = await daily_plan_db.query_by_user_id(user.user_id)
    return daily_plans


@daily_plan_router.get('/daily-plan/{book_name}')
async def query_daily_plan(book_name: str, user: User = Depends(get_current_user)):
    try:
        daily_plan = await daily_plan_db.query_by_user_id_and_book_name(user.user_id, book_name)
        return daily_plan
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Incorrect {error.name}',
        ) from error


@daily_plan_router.post('/daily-plan/{book_name}')
async def add_daily_plan(book_name: str, adding_daily_plan: AddingDailyPlan, user: User = Depends(get_current_user)):
    try:
        daily_plan = await daily_plan_db.insert_by_user_id_and_book_name(user.user_id, book_name, adding_daily_plan)
        return daily_plan
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


@daily_plan_router.patch('/daily-plan/{book_name}')
async def edit_daily_plan(book_name: str, editing_daily_plan: EditingDailyPlan, user: User = Depends(get_current_user)):
    try:
        daily_plan = await daily_plan_db.update_by_user_id_and_book_name(user.user_id, book_name, editing_daily_plan)
        return daily_plan
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


@daily_plan_router.delete('/daily-plan/{book_name}')
async def delete_daily_plan(book_name: str, user: User = Depends(get_current_user)):
    try:
        daily_plan = await daily_plan_db.delete_by_user_id_and_book_name(user.user_id, book_name)
        return daily_plan
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Incorrect {error.name}',
        ) from error


@daily_plan_router.get('/daily-plan/{book_name}/word')
async def query_daily_plan_word(book_name: str, user: User = Depends(get_current_user)):
    try:
        daily_plan = await daily_plan_db.query_by_user_id_and_book_name(user.user_id, book_name)
        word = await word_db.query_by_book_name_and_order(book_name, daily_plan.progress)
        if not daily_plan.is_submitted:
            return WordResponce(
                is_submitted=False,
                book_id=word.book_id,
                word_id=word.word_id,
                spelling=word.spelling,
            )
        else:
            return WordResponce(
                is_submitted=True,
                **word.dict(),
            )
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Incorrect {error.name}',
        ) from error


@daily_plan_router.post('/daily-plan/{book_name}/word')
async def submit_daily_plan_word(book_name: str, user: User = Depends(get_current_user)):
    try:
        await daily_plan_db.update_progress_by_user_id_and_book_name(user.user_id, book_name)
    except NotExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Incorrect {error.name}',
        ) from error

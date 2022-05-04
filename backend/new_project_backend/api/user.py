from fastapi import APIRouter, Depends

from ..model.user import User
from .auth import get_current_user

user_router = APIRouter()


@user_router.get('/user/me')
async def user_me(user: User = Depends(get_current_user)):
    return user

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestFormStrict

from ..db.user import UserNotExistsError, WrongPasswordError, user_db
from ..model.user import UserNoPassword
from ..utils.jwt import InvalidTokenError, create_token, get_user_id_from_token
from .deps import oauth2_password_bearer

auth_router = APIRouter()


async def get_current_user(token: str = Depends(oauth2_password_bearer)):
    try:
        user_id = get_user_id_from_token(token)
        return UserNoPassword.from_user(await user_db.query_by_id(user_id))
    except (InvalidTokenError, UserNotExistsError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from error


@auth_router.post('/token')
async def login(form: OAuth2PasswordRequestFormStrict = Depends()):
    try:
        user = await user_db.verify_name_and_password(form.username, form.password)
        token = create_token(user.user_id, 600)
        return {'access_token': token, 'token_type': 'bearer'}
    except (UserNotExistsError, WrongPasswordError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect user or password',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from error
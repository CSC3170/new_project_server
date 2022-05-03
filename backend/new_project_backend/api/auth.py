from argon2.exceptions import VerificationError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestFormStrict

from ..model.user import User
from ..utils.jwt import create_token, get_user_id_from_token
from ..utils.password import password_hasher
from .deps import oauth2_password_bearer

auth_router = APIRouter()


fake_users_db = [
    {
        'id': 1,
        'name': 'johndoe',
        'hashed_password': password_hasher.hash('password'),
        'nickname': 'John Doe',
        'email': 'johndoe@example.com',
        'phone': None,
    }
]


async def get_user_from_db(username: str, password: str):
    for user in fake_users_db:
        if user['name'] == username:
            try:
                hashed_password = str(user['hashed_password'])
                password_hasher.verify(hashed_password, password)
                if password_hasher.check_needs_rehash(hashed_password):
                    user['hashed_password'] = password_hasher.hash('password')
                return User(**user)
            except VerificationError:
                return None
    return None


async def get_current_user(token: str = Depends(oauth2_password_bearer)):
    user_id = get_user_id_from_token(token)
    for user in fake_users_db:
        if user['id'] == user_id:
            return User(**user)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid authentication credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )


@auth_router.post('/token')
async def login(form: OAuth2PasswordRequestFormStrict = Depends()):
    user = await get_user_from_db(form.username, form.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect user or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    token = create_token(user.id, 600)
    return {'access_token': token, 'token_type': 'bearer'}

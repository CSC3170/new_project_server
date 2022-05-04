from typing import AsyncContextManager, Callable, Optional

from argon2.exceptions import VerificationError
from psycopg import AsyncConnection
from psycopg.errors import UniqueViolation
from psycopg.rows import class_row

from ..model.user import AddingUser, User
from ..utils.password import password_hasher
from .connection import connection_pool


class UserNotExistsError(Exception):
    pass


class WrongPasswordError(Exception):
    pass


class DuplicateRecordError(Exception):
    def __init__(self, record: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.record = record


class UserDB:
    def __init__(self, connection_generator: Callable[..., AsyncContextManager[AsyncConnection]]):
        self._connection_generator = connection_generator
        self._table_name = '"user"'

    async def create(self):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f'''
                        CREATE TABLE IF NOT EXISTS {self._table_name}(
                            user_id BIGSERIAL PRIMARY KEY,
                            name TEXT UNIQUE NOT NULL,
                            hashed_password TEXT NOT NULL,
                            nickname TEXT,
                            email TEXT UNIQUE,
                            phone TEXT UNIQUE
                        );
                    '''
                )

    async def drop(self):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f'''
                        DROP TABLE {self._table_name};
                    '''
                )

    async def insert(self, user: AddingUser):
        hashed_password = password_hasher.hash(user.password)
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(
                        f'''
                            INSERT INTO {self._table_name}(user_id, name, hashed_password, nickname, email, phone)
                            VALUES(DEFAULT, %s, %s, %s, %s, %s)
                            RETURNING user_id;
                        ''',
                        [
                            user.name,
                            hashed_password,
                            user.nickname,
                            user.email,
                            user.phone,
                        ],
                    )
                    result: Optional[tuple[int]] = await cur.fetchone()
                    assert result is not None
                    user_id = result[0]
                    return User(
                        user_id=user_id,
                        name=user.name,
                        hashed_password=hashed_password,
                        nickname=user.nickname,
                        email=user.email,
                        phone=user.phone,
                    )
                except UniqueViolation as error:
                    raise DuplicateRecordError() from error

    async def query_by_id(self, user_id: int):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute(
                    f'''
                        SELECT * FROM {self._table_name} WHERE user_id = %s;
                    ''',
                    [
                        user_id,
                    ],
                )
                user: Optional[User] = await cur.fetchone()
                if user is None:
                    raise UserNotExistsError()
                return user

    async def query_by_name(self, name: int):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute(
                    f'''
                        SELECT * FROM {self._table_name} WHERE name = %s;
                    ''',
                    [
                        name,
                    ],
                )
                user: Optional[User] = await cur.fetchone()
                if user is None:
                    raise UserNotExistsError()
                return user

    async def verify_id_and_password(self, user_id: str, password: str):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute(
                    f'''
                        SELECT * FROM {self._table_name} WHERE user_id = %s;
                    ''',
                    [
                        user_id,
                    ],
                )
                user: Optional[User] = await cur.fetchone()
                if user is None:
                    raise UserNotExistsError()
                try:
                    if password_hasher.check_needs_rehash(user.hashed_password):
                        user.hashed_password = password_hasher.hash(password)
                        await cur.execute(
                            f'''
                                UPDATE {self._table_name} SET hashed_password = %s WHERE id = %s;
                            ''',
                            [
                                user.hashed_password,
                                user.user_id,
                            ],
                        )
                    return user
                except VerificationError as error:
                    raise WrongPasswordError() from error

    async def verify_name_and_password(self, name: str, password: str):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute(
                    f'''
                        SELECT * FROM {self._table_name} WHERE name = %s;
                    ''',
                    [
                        name,
                    ],
                )
                user: Optional[User] = await cur.fetchone()
                if user is None:
                    raise UserNotExistsError()
                try:
                    password_hasher.verify(user.hashed_password, password)
                    if password_hasher.check_needs_rehash(user.hashed_password):
                        user.hashed_password = password_hasher.hash(password)
                        await cur.execute(
                            f'''
                                UPDATE {self._table_name} SET hashed_password = %s WHERE id = %s;
                            ''',
                            [
                                user.hashed_password,
                                user.user_id,
                            ],
                        )
                    return user
                except VerificationError as error:
                    raise WrongPasswordError() from error


user_db = UserDB(connection_pool.connection)

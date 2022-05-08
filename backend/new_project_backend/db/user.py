from typing import AsyncContextManager, Callable

from argon2.exceptions import VerificationError
from psycopg import AsyncConnection
from psycopg.errors import UniqueViolation
from psycopg.rows import class_row

from ..model.user import AddingUser, EditingUser, User
from ..utils.password import password_hasher
from .connection import connection_pool
from .errors import DuplicateRecordError, NotExistsError


class WrongPasswordError(Exception):
    pass


class UserDB:
    def __init__(self, connection_generator: Callable[..., AsyncContextManager[AsyncConnection]]):
        self._connection_generator = connection_generator

    async def create(self):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS "user"(
                            "user_id" BIGSERIAL PRIMARY KEY,
                            "name" TEXT UNIQUE NOT NULL,
                            "hashed_password" TEXT NOT NULL,
                            "is_admin" BOOLEAN DEFAULT FALSE,
                            "nickname" TEXT,
                            "email" TEXT UNIQUE,
                            "phone" TEXT UNIQUE
                        );
                    '''
                )

    async def drop(self):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''
                        DROP TABLE IF EXISTS "user";
                    '''
                )

    async def insert(self, adding_user: AddingUser):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                adding_user_dict = adding_user.dict()
                password = adding_user_dict.pop('password')
                adding_user_dict['hashed_password'] = password_hasher.hash(password)
                try:
                    await cur.execute(
                        f'''
                            INSERT INTO "user"(
                                {', '.join([f'"{key}"' for key in adding_user_dict.keys()])}
                            )
                            VALUES(
                                {', '.join(['%s'] * len(adding_user_dict))}
                            )
                            RETURNING *;
                        ''',
                        [
                            *adding_user_dict.values(),
                        ],
                    )
                    user = await cur.fetchone()
                    assert user is not None
                    if user.user_id == 1:
                        await cur.execute(
                            '''
                                UPDATE "user"
                                SET "is_admin" = %s
                                WHERE "user_id" = %s
                                RETURNING *;
                            ''',
                            [
                                True,
                                1,
                            ],
                        )
                        user = await cur.fetchone()
                        assert user is not None
                    return user
                except UniqueViolation as error:
                    raise DuplicateRecordError() from error

    async def update_by_user_id(self, user_id: int, editing_user: EditingUser):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                editing_user_dict = editing_user.dict(exclude_unset=True)
                if not editing_user_dict:
                    await cur.execute(
                        '''
                            SELECT * FROM "user"
                            WHERE "user_id" = %s;
                        ''',
                        [
                            user_id,
                        ],
                    )
                else:
                    if 'password' in editing_user_dict:
                        password = editing_user_dict.pop('password')
                        editing_user_dict['hashed_password'] = password_hasher.hash(password)
                    try:
                        await cur.execute(
                            f'''
                                UPDATE "user"
                                SET {', '.join([f'"{key}" = %s' for key in editing_user_dict.keys()])}
                                WHERE "user_id" = %s
                                RETURNING *;
                            ''',
                            [
                                *editing_user_dict.values(),
                                user_id,
                            ],
                        )
                    except UniqueViolation as error:
                        raise DuplicateRecordError() from error
                user = await cur.fetchone()
                if user is None:
                    raise NotExistsError('user')
                return user

    async def update_by_name(self, name: str, editing_user: EditingUser):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                editing_user_dict = editing_user.dict(exclude_unset=True)
                if not editing_user_dict:
                    await cur.execute(
                        '''
                            SELECT * FROM "user"
                            WHERE "name" = %s;
                        ''',
                        [
                            name,
                        ],
                    )
                else:
                    if 'password' in editing_user_dict:
                        password = editing_user_dict.pop('password')
                        editing_user_dict['hashed_password'] = password_hasher.hash(password)
                    try:
                        await cur.execute(
                            f'''
                                UPDATE "user"
                                SET {', '.join([f'"{key}" = %s' for key in editing_user_dict.keys()])}
                                WHERE "name" = %s
                                RETURNING *;
                            ''',
                            [
                                *editing_user_dict.values(),
                                name,
                            ],
                        )
                    except UniqueViolation as error:
                        raise DuplicateRecordError() from error
                user = await cur.fetchone()
                if user is None:
                    raise NotExistsError('user')
                return user

    async def delete_by_user_id(self, user_id: int):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute(
                    '''
                        DELETE FROM "user"
                        WHERE "user_id" = %s
                        RETURNING *;
                    ''',
                    [
                        user_id,
                    ],
                )
                user = await cur.fetchone()
                if user is None:
                    raise NotExistsError('user')
                return user

    async def delete_by_name(self, name: str):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute(
                    '''
                        DELETE FROM "user"
                        WHERE "name" = %s
                        RETURNING *;
                    ''',
                    [
                        name,
                    ],
                )
                user = await cur.fetchone()
                if user is None:
                    raise NotExistsError('user')
                return user

    async def query_by_user_id(self, user_id: int):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute(
                    '''
                        SELECT * FROM "user"
                        WHERE "user_id" = %s;
                    ''',
                    [
                        user_id,
                    ],
                )
                user = await cur.fetchone()
                if user is None:
                    raise NotExistsError('user')
                return user

    async def query_by_name(self, name: str):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute(
                    '''
                        SELECT * FROM "user"
                        WHERE "name" = %s;
                    ''',
                    [
                        name,
                    ],
                )
                user = await cur.fetchone()
                if user is None:
                    raise NotExistsError('user')
                return user

    async def verify_user_id_and_password(self, user_id: int, password: str):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute(
                    '''
                        SELECT * FROM "user"
                        WHERE "user_id" = %s;
                    ''',
                    [
                        user_id,
                    ],
                )
                user = await cur.fetchone()
                if user is None:
                    raise NotExistsError('user')
                try:
                    password_hasher.verify(user.hashed_password, password)
                    if password_hasher.check_needs_rehash(user.hashed_password):
                        user.hashed_password = password_hasher.hash(password)
                        await cur.execute(
                            '''
                                UPDATE "user"
                                SET "hashed_password" = %s
                                WHERE "user_id" = %s
                                RETURNING *;
                            ''',
                            [
                                user.hashed_password,
                                user.user_id,
                            ],
                        )
                        user = await cur.fetchone()
                        assert user is not None
                    return user
                except VerificationError as error:
                    raise WrongPasswordError() from error

    async def verify_name_and_password(self, name: str, password: str):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute(
                    '''
                        SELECT * FROM "user"
                        WHERE "name" = %s;
                    ''',
                    [
                        name,
                    ],
                )
                user = await cur.fetchone()
                if user is None:
                    raise NotExistsError('user')
                try:
                    password_hasher.verify(user.hashed_password, password)
                    if password_hasher.check_needs_rehash(user.hashed_password):
                        user.hashed_password = password_hasher.hash(password)
                        await cur.execute(
                            '''
                                UPDATE "user"
                                SET "hashed_password" = %s
                                WHERE "user_id" = %s
                                RETURNING *;
                            ''',
                            [
                                user.hashed_password,
                                user.user_id,
                            ],
                        )
                        user = await cur.fetchone()
                        assert user is not None
                    return user
                except VerificationError as error:
                    raise WrongPasswordError() from error


user_db = UserDB(connection_pool.connection)

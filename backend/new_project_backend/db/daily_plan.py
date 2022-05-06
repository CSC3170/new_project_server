from typing import AsyncContextManager, Callable

from psycopg import AsyncConnection
from psycopg.errors import UniqueViolation
from psycopg.rows import class_row

from ..model.book import Book
from ..model.daily_plan import AddingDailyPlan, DailyPlan, EditingDailyPlan
from ..model.user import User
from .connection import connection_pool
from .errors import DuplicateRecordError, NotExistsError


class DailyPlanDB:
    def __init__(self, connection_generator: Callable[..., AsyncContextManager[AsyncConnection]]):
        self._connection_generator = connection_generator

    async def create(self):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS "daily_plan"(
                            "user_id" BIGINT REFERENCES "user"("user_id"),
                            "book_id" BIGINT REFERENCES "book"("book_id"),
                            "daily_goal" BIGINT NOT NULL,
                            "progress" BIGINT NOT NULL DEFAULT 0,
                            PRIMARY KEY ("user_id", "book_id")
                        );

                        CREATE TABLE IF NOT EXISTS "daily_plan_evaluation_detail"(
                            "evaluation_id" BIGSERIAL PRIMARY KEY,
                            "date" TIMESTAMP UNIQUE NOT NULL,
                            "daily_goal" BIGINT NOT NULL,
                            "daily_progress" BIGINT NOT NULL
                        );

                        CREATE TABLE IF NOT EXISTS "daily_plan_evaluation"(
                            "user_id" BIGINT NOT NULL REFERENCES "user"("user_id"),
                            "book_id" BIGINT NOT NULL REFERENCES "book"("book_id"),
                            "evaluation_id" BIGINT NOT NULL REFERENCES "daily_plan_evaluation_detail"("evaluation_id"),
                            PRIMARY KEY ("user_id", "book_id", "evaluation_id")
                        );
                    '''
                )

    async def drop(self):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''
                        DROP TABLE IF EXISTS "daily_plan_evaluation";
                        DROP TABLE IF EXISTS "daily_plan_evaluation_detail";
                        DROP TABLE IF EXISTS "daily_plan";
                    '''
                )

    async def insert_by_user_id_and_book_name(self, user_id: int, book_name: str, adding_daily_plan: AddingDailyPlan):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                cur.row_factory = class_row(User)
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
                cur.row_factory = class_row(Book)
                await cur.execute(
                    '''
                        SELECT * FROM "book"
                        WHERE "name" = %s;
                    ''',
                    [
                        book_name,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError('book')
                cur.row_factory = class_row(DailyPlan)
                adding_daily_plan_dict = adding_daily_plan.dict()
                try:
                    await cur.execute(
                        f'''
                            INSERT INTO "daily_plan"(
                                "user_id",
                                "book_id",
                                {', '.join([f'"{key}"' for key in adding_daily_plan_dict.keys()])}
                            )
                            VALUES(
                                %s,
                                %s,
                                {', '.join(['%s'] * len(adding_daily_plan_dict))}
                            )
                            RETURNING *;
                        ''',
                        [
                            user.user_id,
                            book.book_id,
                            *adding_daily_plan_dict.values(),
                        ],
                    )
                    word = await cur.fetchone()
                    assert word is not None
                    return word
                except UniqueViolation as error:
                    raise DuplicateRecordError() from error

    async def update_by_user_id_and_book_name(self, user_id: int, book_name: str, editing_daily_plan: EditingDailyPlan):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                cur.row_factory = class_row(User)
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
                cur.row_factory = class_row(Book)
                await cur.execute(
                    '''
                        SELECT * FROM "book"
                        WHERE "name" = %s;
                    ''',
                    [
                        book_name,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError('book')
                cur.row_factory = class_row(DailyPlan)
                editing_daily_plan_dict = editing_daily_plan.dict(exclude_unset=True)
                if not editing_daily_plan_dict:
                    await cur.execute(
                        '''
                            SELECT * FROM "daily_plan"
                            WHERE "user_id" = %s
                            AND "book_id" = %s;
                        ''',
                        [
                            user.user_id,
                            book.book_id,
                        ],
                    )
                else:
                    try:
                        await cur.execute(
                            f'''
                                UPDATE "daily_plan"
                                SET {', '.join([f'"{key}" = %s' for key in editing_daily_plan_dict.keys()])}
                                WHERE "user_id" = %s
                                AND "book_id" = %s
                                RETURNING *;
                            ''',
                            [
                                *editing_daily_plan_dict.values(),
                                user.user_id,
                                book.book_id,
                            ],
                        )
                    except UniqueViolation as error:
                        raise DuplicateRecordError() from error
                daily_plan = await cur.fetchone()
                if daily_plan is None:
                    raise NotExistsError('daily plan')
                return daily_plan

    async def delete_by_user_id_and_book_name(self, user_id: int, book_name: str):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                cur.row_factory = class_row(User)
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
                cur.row_factory = class_row(Book)
                await cur.execute(
                    '''
                        SELECT * FROM "book"
                        WHERE "name" = %s;
                    ''',
                    [
                        book_name,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError('book')
                cur.row_factory = class_row(DailyPlan)
                await cur.execute(
                    '''
                        DELETE FROM "daily_plan"
                        WHERE "user_id" = %s
                        AND "book_id" = %s
                        RETURNING *;
                    ''',
                    [
                        user.user_id,
                        book.book_id,
                    ],
                )
                daily_plan = await cur.fetchone()
                if daily_plan is None:
                    raise NotExistsError('daily plan')
                return daily_plan

    async def query_by_user_id(self, user_id: int):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                cur.row_factory = class_row(User)
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
                cur.row_factory = class_row(DailyPlan)
                await cur.execute(
                    '''
                        SELECT * FROM "daily_plan"
                        WHERE "user_id" = %s;
                    ''',
                    [
                        user.user_id,
                    ],
                )
                daily_plans = await cur.fetchall()
                return daily_plans

    async def query_by_user_id_and_book_name(self, user_id: int, book_name: str):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                cur.row_factory = class_row(User)
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
                cur.row_factory = class_row(Book)
                await cur.execute(
                    '''
                        SELECT * FROM "book"
                        WHERE "name" = %s;
                    ''',
                    [
                        book_name,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError('book')
                cur.row_factory = class_row(DailyPlan)
                await cur.execute(
                    '''
                        SELECT * FROM "daily_plan"
                        WHERE "user_id" = %s
                        AND "book_id" = %s;
                    ''',
                    [
                        user.user_id,
                        book.book_id,
                    ],
                )
                daily_plan = await cur.fetchone()
                if daily_plan is None:
                    raise NotExistsError('daily plan')
                return daily_plan

    async def update_progress_by_user_id_and_book_name(self, user_id: int, book_name: str):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                cur.row_factory = class_row(User)
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
                cur.row_factory = class_row(Book)
                await cur.execute(
                    '''
                        SELECT * FROM "book"
                        WHERE "name" = %s;
                    ''',
                    [
                        book_name,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError('book')
                cur.row_factory = class_row(DailyPlan)
                await cur.execute(
                    '''
                        UPDATE "daily_plan"
                        SET "progress" = "progress" + 1
                        WHERE "user_id" = %s
                        AND "book_id" = %s
                        RETURNING *;
                    ''',
                    [
                        user.user_id,
                        book.book_id,
                    ],
                )
                daily_plan = await cur.fetchone()
                if daily_plan is None:
                    raise NotExistsError('daily plan')
                return daily_plan


daily_plan_db = DailyPlanDB(connection_pool.connection)

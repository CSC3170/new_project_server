from typing import AsyncContextManager, Callable

from psycopg import AsyncConnection
from psycopg.errors import UniqueViolation
from psycopg.rows import class_row

from ..model.book import AddingBook, Book, EditingBook
from .base import DBBase, DuplicateRecordError, NotExistsError
from .connection import connection_pool


class BookDB(DBBase):
    def __init__(self, connection_generator: Callable[..., AsyncContextManager[AsyncConnection]]):
        super().__init__(connection_generator, 'book')

    async def create(self):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f'''
                        CREATE TABLE IF NOT EXISTS {self._table_name}(
                            book_id BIGSERIAL PRIMARY KEY,
                            name TEXT UNIQUE NOT NULL,
                            description TEXT,
                            word_count BIGINT NOT NULL
                        );
                    '''
                )

    async def insert(self, adding_book: AddingBook):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(Book)) as cur:
                adding_book_dict = adding_book.dict()
                try:
                    await cur.execute(
                        f'''
                            INSERT INTO {self._table_name}(book_id, {', '.join(adding_book_dict.keys())})
                            VALUES(DEFAULT, {', '.join(['%s'] * len(adding_book_dict))})
                            RETURNING *;
                        ''',
                        [
                            *adding_book_dict.values(),
                        ],
                    )
                    book = await cur.fetchone()
                    assert book is not None
                    return book
                except UniqueViolation as error:
                    raise DuplicateRecordError() from error

    async def update_by_book_id(self, book_id: int, editing_book: EditingBook):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(Book)) as cur:
                editing_book_dict = editing_book.dict(exclude_unset=True)
                if not editing_book_dict:
                    await cur.execute(
                        f'''
                            SELECT * FROM {self._table_name}
                            WHERE book_id = %s;
                        ''',
                        [
                            book_id,
                        ],
                    )
                else:
                    try:
                        await cur.execute(
                            f'''
                                UPDATE {self._table_name}
                                SET {', '.join([f'{key} = %s' for key in editing_book_dict.keys()])}
                                WHERE book_id = %s
                                RETURNING *;
                            ''',
                            [
                                *editing_book_dict.values(),
                                book_id,
                            ],
                        )
                    except UniqueViolation as error:
                        raise DuplicateRecordError() from error
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError()
                return book

    async def update_by_name(self, name: str, editing_book: EditingBook):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(Book)) as cur:
                editing_book_dict = editing_book.dict(exclude_unset=True)
                if not editing_book_dict:
                    await cur.execute(
                        f'''
                            SELECT * FROM {self._table_name}
                            WHERE name = %s;
                        ''',
                        [
                            name,
                        ],
                    )
                else:
                    try:
                        await cur.execute(
                            f'''
                                UPDATE {self._table_name}
                                SET {', '.join([f'{key} = %s' for key in editing_book_dict.keys()])}
                                WHERE name = %s
                                RETURNING *;
                            ''',
                            [
                                *editing_book_dict.values(),
                                name,
                            ],
                        )
                    except UniqueViolation as error:
                        raise DuplicateRecordError() from error
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError()
                return book

    async def delete_by_book_id(self, book_id: int):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(Book)) as cur:
                await cur.execute(
                    f'''
                        DELETE FROM {self._table_name}
                        WHERE book_id = %s
                        RETURNING *;
                    ''',
                    [
                        book_id,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError()
                return book

    async def delete_by_name(self, name: str):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(Book)) as cur:
                await cur.execute(
                    f'''
                        DELETE FROM {self._table_name}
                        WHERE name = %s
                        RETURNING *;
                    ''',
                    [
                        name,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError()
                return book

    async def query(self):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(Book)) as cur:
                await cur.execute(
                    f'''
                        SELECT * FROM {self._table_name};
                    '''
                )
                books = await cur.fetchall()
                return books

    async def query_by_book_id(self, book_id: int):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(Book)) as cur:
                await cur.execute(
                    f'''
                        SELECT * FROM {self._table_name}
                        WHERE book_id = %s;
                    ''',
                    [
                        book_id,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError()
                return book

    async def query_by_name(self, name: str):
        async with self._connection_generator() as conn:
            async with conn.cursor(row_factory=class_row(Book)) as cur:
                await cur.execute(
                    f'''
                        SELECT * FROM {self._table_name}
                        WHERE name = %s;
                    ''',
                    [
                        name,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError()
                return book


book_db = BookDB(connection_pool.connection)
from typing import AsyncContextManager, Callable

from psycopg import AsyncConnection
from psycopg.errors import UniqueViolation
from psycopg.rows import class_row

from ..model.book import Book
from ..model.word import AddingWord, EditingWord, Word
from .connection import connection_pool
from .errors import DuplicateRecordError, NotExistsError


class WordDB:
    def __init__(self, connection_generator: Callable[..., AsyncContextManager[AsyncConnection]]):
        self._connection_generator = connection_generator

    async def create(self):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS "word"(
                            "book_id" BIGINT NOT NULL REFERENCES "book"("book_id"),
                            "word_id" BIGINT NOT NULL,
                            "spelling" TEXT NOT NULL,
                            "translation" TEXT,
                            PRIMARY KEY ("book_id", "word_id")
                        );

                        CREATE OR REPLACE FUNCTION "fill_in_word_seq"()
                        RETURNS TRIGGER
                        LANGUAGE PLPGSQL
                        AS $$
                        BEGIN
                            NEW."word_id" := nextval('"book_seq_' || NEW.book_id || '"');
                            RETURN NEW;
                        END
                        $$;

                        CREATE OR REPLACE TRIGGER "fill_in_word_seq"
                        BEFORE INSERT ON "word"
                        FOR EACH ROW EXECUTE PROCEDURE "fill_in_word_seq"();

                        CREATE OR REPLACE FUNCTION "update_words_count_after_insert"()
                        RETURNS TRIGGER
                        LANGUAGE PLPGSQL
                        AS $$
                        BEGIN
                            UPDATE "book"
                            SET "words_count" = "words_count" + 1
                            WHERE "book_id" = NEW."book_id";
                            RETURN NEW;
                        END
                        $$;

                        CREATE OR REPLACE TRIGGER "update_words_count_after_insert"
                        AFTER INSERT ON "word"
                        FOR EACH ROW EXECUTE procedure "update_words_count_after_insert"();

                        CREATE OR REPLACE FUNCTION "update_words_count_after_delete"()
                        RETURNS TRIGGER
                        LANGUAGE PLPGSQL
                        AS $$
                        BEGIN
                            UPDATE "book"
                            SET "words_count" = "words_count" - 1
                            WHERE "book_id" = OLD."book_id";
                            RETURN OLD;
                        END
                        $$;

                        CREATE OR REPLACE TRIGGER "update_words_count_after_delete"
                        AFTER DELETE ON "word"
                        FOR EACH ROW EXECUTE procedure "update_words_count_after_delete"();
                    '''
                )

    async def drop(self):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''
                        DROP TABLE IF EXISTS "word";
                        DROP FUNCTION IF EXISTS "fill_in_word_seq";
                    '''
                )

    async def insert_by_book_id(self, book_id: int, adding_word: AddingWord):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                cur.row_factory = class_row(Book)
                await cur.execute(
                    '''
                        SELECT * FROM "book"
                        WHERE "book_id" = %s;
                    ''',
                    [
                        book_id,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError('book')
                cur.row_factory = class_row(Word)
                adding_word_dict = adding_word.dict()
                try:
                    await cur.execute(
                        f'''
                            INSERT INTO word(
                                book_id,
                                {', '.join([f'"{key}"' for key in adding_word_dict.keys()])}
                            )
                            VALUES(
                                %s,
                                {', '.join(['%s'] * len(adding_word_dict))}
                            )
                            RETURNING *;
                        ''',
                        [
                            book.book_id,
                            *adding_word_dict.values(),
                        ],
                    )
                    word = await cur.fetchone()
                    assert word is not None
                    return word
                except UniqueViolation as error:
                    raise DuplicateRecordError() from error

    async def insert_by_book_name(self, book_name: str, adding_word: AddingWord):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
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
                cur.row_factory = class_row(Word)
                adding_word_dict = adding_word.dict()
                try:
                    await cur.execute(
                        f'''
                            INSERT INTO "word"(
                                "book_id",
                                {', '.join([f'"{key}"' for key in adding_word_dict.keys()])}
                            )
                            VALUES(
                                %s,
                                {', '.join(['%s'] * len(adding_word_dict))}
                            )
                            RETURNING *;
                        ''',
                        [
                            book.book_id,
                            *adding_word_dict.values(),
                        ],
                    )
                    word = await cur.fetchone()
                    assert word is not None
                    return word
                except UniqueViolation as error:
                    raise DuplicateRecordError() from error

    async def update_by_book_id_and_word_id(self, book_id: int, word_id: int, editing_word: EditingWord):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                cur.row_factory = class_row(Book)
                await cur.execute(
                    '''
                        SELECT * FROM "book"
                        WHERE "book_id" = %s;
                    ''',
                    [
                        book_id,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError('book')
                cur.row_factory = class_row(Word)
                editing_word_dict = editing_word.dict(exclude_unset=True)
                if not editing_word_dict:
                    await cur.execute(
                        '''
                            SELECT * FROM "word"
                            WHERE "book_id" = %s
                            AND "word_id" = %s;
                        ''',
                        [
                            book.book_id,
                            word_id,
                        ],
                    )
                else:
                    try:
                        await cur.execute(
                            f'''
                                UPDATE "word"
                                SET {', '.join([f'"{key}" = %s' for key in editing_word_dict.keys()])}
                                WHERE "book_id" = %s
                                AND "word_id" = %s
                                RETURNING *;
                            ''',
                            [
                                *editing_word_dict.values(),
                                book.book_id,
                                word_id,
                            ],
                        )
                    except UniqueViolation as error:
                        raise DuplicateRecordError() from error
                word = await cur.fetchone()
                if word is None:
                    raise NotExistsError('word')
                return word

    async def update_by_book_name_and_word_id(self, book_name: str, word_id: int, editing_word: EditingWord):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
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
                cur.row_factory = class_row(Word)
                editing_word_dict = editing_word.dict(exclude_unset=True)
                if not editing_word_dict:
                    await cur.execute(
                        '''
                            SELECT * FROM "word"
                            WHERE "book_id" = %s
                            AND "word_id" = %s;
                        ''',
                        [
                            book.book_id,
                            word_id,
                        ],
                    )
                else:
                    try:
                        await cur.execute(
                            f'''
                                UPDATE "word"
                                SET {', '.join([f'"{key}" = %s' for key in editing_word_dict.keys()])}
                                WHERE "book_id" = %s
                                AND "word_id" = %s
                                RETURNING *;
                            ''',
                            [
                                *editing_word_dict.values(),
                                book.book_id,
                                word_id,
                            ],
                        )
                    except UniqueViolation as error:
                        raise DuplicateRecordError() from error
                word = await cur.fetchone()
                if word is None:
                    raise NotExistsError('word')
                return word

    async def delete_by_book_id(self, book_id: int):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                cur.row_factory = class_row(Book)
                await cur.execute(
                    '''
                        SELECT * FROM "book"
                        WHERE "book_id" = %s;
                    ''',
                    [
                        book_id,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError('book')
                cur.row_factory = class_row(Word)
                await cur.execute(
                    '''
                        DELETE FROM "word"
                        WHERE "book_id" = %s
                        RETURNING *;
                    ''',
                    [
                        book.book_id,
                    ],
                )
                words = await cur.fetchall()
                return words

    async def delete_by_book_name(self, book_name: str):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
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
                cur.row_factory = class_row(Word)
                await cur.execute(
                    '''
                        DELETE FROM "word"
                        WHERE "book_id" = %s
                        RETURNING *;
                    ''',
                    [
                        book.book_id,
                    ],
                )
                words = await cur.fetchall()
                return words

    async def delete_by_book_id_and_word_id(self, book_id: int, word_id: int):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                cur.row_factory = class_row(Book)
                await cur.execute(
                    '''
                        SELECT * FROM "book"
                        WHERE "book_id" = %s;
                    ''',
                    [
                        book_id,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError('book')
                cur.row_factory = class_row(Word)
                await cur.execute(
                    '''
                        DELETE FROM "word"
                        WHERE "book_id" = %s
                        AND "word_id" = %s
                        RETURNING *;
                    ''',
                    [
                        book.book_id,
                        word_id,
                    ],
                )
                word = await cur.fetchone()
                if word is None:
                    raise NotExistsError('word')
                return word

    async def delete_by_book_name_and_word_id(self, book_name: str, word_id: int):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
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
                cur.row_factory = class_row(Word)
                await cur.execute(
                    '''
                        DELETE FROM "word"
                        WHERE "book_id" = %s
                        AND "word_id" = %s
                        RETURNING *;
                    ''',
                    [
                        book.book_id,
                        word_id,
                    ],
                )
                word = await cur.fetchone()
                if word is None:
                    raise NotExistsError('word')
                return word

    async def query_by_book_id(self, book_id: int):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                cur.row_factory = class_row(Book)
                await cur.execute(
                    '''
                        SELECT * FROM "book"
                        WHERE "book_id" = %s;
                    ''',
                    [
                        book_id,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError('book')
                cur.row_factory = class_row(Word)
                await cur.execute(
                    '''
                        SELECT * FROM "word"
                        WHERE "book_id" = %s;
                    ''',
                    [
                        book.book_id,
                    ],
                )
                words = await cur.fetchall()
                return words

    async def query_by_book_name(self, book_name: str):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
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
                cur.row_factory = class_row(Word)
                await cur.execute(
                    '''
                        SELECT * FROM "word"
                        WHERE "book_id" = %s;
                    ''',
                    [
                        book.book_id,
                    ],
                )
                words = await cur.fetchall()
                return words

    async def query_by_book_id_and_word_id(self, book_id: int, word_id: int):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                cur.row_factory = class_row(Book)
                await cur.execute(
                    '''
                        SELECT * FROM "book"
                        WHERE "book_id" = %s;
                    ''',
                    [
                        book_id,
                    ],
                )
                book = await cur.fetchone()
                if book is None:
                    raise NotExistsError('book')
                cur.row_factory = class_row(Word)
                await cur.execute(
                    '''
                        SELECT * FROM "word"
                        WHERE "book_id" = %s
                        AND "word_id" = %s;
                    ''',
                    [
                        book.book_id,
                        word_id,
                    ],
                )
                word = await cur.fetchone()
                if word is None:
                    raise NotExistsError('word')
                return word

    async def query_by_book_name_and_word_id(self, book_name: str, word_id: int):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
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
                cur.row_factory = class_row(Word)
                await cur.execute(
                    '''
                        SELECT * FROM "word"
                        WHERE "book_id" = %s
                        AND "word_id" = %s;
                    ''',
                    [
                        book.book_id,
                        word_id,
                    ],
                )
                word = await cur.fetchone()
                if word is None:
                    raise NotExistsError('word')
                return word


word_db = WordDB(connection_pool.connection)

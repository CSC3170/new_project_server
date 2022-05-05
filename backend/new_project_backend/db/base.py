from typing import AsyncContextManager, Callable

from psycopg import AsyncConnection


class DBBase:
    def __init__(self, connection_generator: Callable[..., AsyncContextManager[AsyncConnection]], table_name: str):
        self._connection_generator = connection_generator
        self._table_name = table_name

    async def drop(self):
        async with self._connection_generator() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f'''
                        DROP TABLE {self._table_name};
                    '''
                )

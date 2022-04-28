from psycopg_pool import AsyncConnectionPool

from .config import DBNAME, HOST, PASSWORD, PORT, USER

connection_pool = AsyncConnectionPool(
    conninfo=f'host={HOST} port={PORT} dbname={DBNAME} user={USER} password={PASSWORD}', open=False
)

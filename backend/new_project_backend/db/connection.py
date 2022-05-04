from psycopg_pool import AsyncConnectionPool

from ..config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

connection_pool = AsyncConnectionPool(
    conninfo=f'host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}', open=False
)

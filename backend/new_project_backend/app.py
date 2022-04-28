from fastapi import FastAPI

from .api.test import test_router
from .db.connection import connection_pool

app = FastAPI()
app.include_router(test_router, prefix='/api')


@app.on_event('startup')
def open_pool():
    connection_pool.open()


@app.on_event('shutdown')
def close_pool():
    connection_pool.close()

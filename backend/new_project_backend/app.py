from fastapi import FastAPI

from .api.auth import auth_router
from .api.test import test_router
from .api.user import user_router
from .db.connection import connection_pool

app = FastAPI()
app.include_router(test_router, prefix='/api')
app.include_router(user_router, prefix='/api')
app.include_router(auth_router, prefix='/api')


@app.on_event('startup')
async def startup():
    await connection_pool.open()


@app.on_event('shutdown')
async def shutdown():
    await connection_pool.close()

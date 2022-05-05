from fastapi import FastAPI

from .api.auth import auth_router
from .api.test import test_router
from .api.user import user_router
from .db.connection import connection_pool
from .db.user import user_db
from .utils.key import private_key

app = FastAPI()
app.include_router(test_router, prefix='/api')
app.include_router(user_router, prefix='/api')
app.include_router(auth_router, prefix='/api')


@app.on_event('startup')
async def startup():
    await connection_pool.open()
    await user_db.create()
    private_key.initialize()


@app.on_event('shutdown')
async def shutdown():
    await connection_pool.close()

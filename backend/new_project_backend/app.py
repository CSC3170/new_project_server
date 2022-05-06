from fastapi import FastAPI

from .api.auth import auth_router
from .api.book import book_router
from .api.daily_plan import daily_plan_router
from .api.user import user_router
from .api.word import word_router
from .db.book import book_db
from .db.connection import connection_pool
from .db.daily_plan import daily_plan_db
from .db.user import user_db
from .db.word import word_db
from .utils.key import private_key

app = FastAPI()
app.include_router(auth_router, prefix='/api')
app.include_router(user_router, prefix='/api')
app.include_router(book_router, prefix='/api')
app.include_router(word_router, prefix='/api')
app.include_router(daily_plan_router, prefix='/api')


@app.on_event('startup')
async def startup():
    await connection_pool.open()
    # await word_db.drop()
    # await book_db.drop()
    # await user_db.drop()
    # await daily_plan_db.drop()
    await user_db.create()
    await book_db.create()
    await word_db.create()
    await daily_plan_db.create()
    private_key.initialize()


@app.on_event('shutdown')
async def shutdown():
    await connection_pool.close()

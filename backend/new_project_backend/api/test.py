from fastapi import APIRouter

test_router = APIRouter()


@test_router.get('/test')
async def test():
    return {'data': 'test'}


@test_router.get('/test/{item}')
async def test_id(item: int):
    return {'data': f'test-{item}'}

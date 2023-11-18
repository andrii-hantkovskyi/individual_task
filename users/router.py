from fastapi import APIRouter

from users.models import UserCreate, UserLogin
from users.services import create_user, login_user

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.post('/', status_code=201)
async def create_users(user_data: UserCreate):
    return await create_user(user_data)


@users_router.post('/login')
async def login(login_data: UserLogin):
    try:
        return await login_user(login_data)
    except ValueError as e:
        print(e)
        return {'error': str(e)}

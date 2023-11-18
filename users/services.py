import bcrypt
import jwt

import settings
from database import database
from users.models import UserCreate, UserJWT, UserLogin

collection = database.users


async def get_user_by_email(email: str):
    user = await collection.find_one({'email': email})
    return user


async def create_user(user_data: UserCreate):
    if await get_user_by_email(user_data.email):
        raise ValueError('User with such email already registered')

    user_data.password = bcrypt.hashpw(user_data.password.encode('utf-8'), salt=settings.SECRET_TOKEN.encode('utf-8'))
    await collection.insert_one(user_data.model_dump(mode='python'))


async def login_user(login_data: UserLogin):
    email, password = login_data.email, login_data.password
    user = await get_user_by_email(email)

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        raise ValueError('Wrong credentials')

    token = jwt.encode(UserJWT(**user).model_dump(mode='json'), key=settings.SECRET_TOKEN, algorithm='HS256')
    return token

import datetime
from typing import List

import bcrypt
import jwt
from bson import ObjectId

import settings
from database import database
from users.models import UserCreate, UserJWT, UserLogin, UserUpdate, RoleTypes, User

collection = database.users


async def get_user_by_email(email: str):
    user = await collection.find_one({'email': email})
    return user


async def get_user_by_id(user_id: str):
    return await collection.find_one({'_id': ObjectId(user_id)})


async def _get_users_by_birth_month(birth_month: int) -> List[User]:
    res = []
    cursor = collection.find(
        {'date_of_birth': {'$regex': f".-{birth_month if len(str(birth_month)) == 2 else f"0{birth_month}"}-."}})

    async for user in cursor:
        res.append(User(**user))

    return res


async def delete_user_by_email(email: str):
    await collection.delete_one({'email': email})


async def delete_user_by_id(user_id: str):
    await collection.delete_one({'_id': ObjectId(user_id)})


async def create_user(user_data: UserCreate):
    if await get_user_by_email(user_data.email):
        raise ValueError('User with such email already registered')

    user_data.password = bcrypt.hashpw(user_data.password.encode('utf-8'), salt=settings.SECRET_TOKEN.encode('utf-8'))
    if not (settings.DEBUG and user_data.role == RoleTypes.test.value):
        user_data.role = RoleTypes.user
    user_data.date_of_birth = datetime.date.strftime(user_data.date_of_birth, settings.DATE_FORMAT)
    await collection.insert_one(user_data.model_dump(mode='python'))


async def get_jwt_token(login_data: UserLogin):
    email, password = login_data.email, login_data.password
    user = await get_user_by_email(email)

    if not user:
        raise ValueError('Wrong credentials')

    if user.get('login_unsuccessful_attempts', 0) >= 3:
        raise ValueError('Reached login attempts limit')
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        await collection.update_one(
            {'email': user['email']},
            {'$set': {
                'login_unsuccessful_attempts': user.get('login_unsuccessful_attempts', 0) + 1
            }}
        )
        raise ValueError('Wrong credentials')

    await collection.update_one({'email': user['email']}, {'$set': {'login_unsuccessful_attempts': 0}})
    token = jwt.encode(UserJWT(**user).model_dump(mode='json'), key=settings.SECRET_TOKEN,
                       algorithm=settings.JWT_ALGORITHM)
    return token


async def update_user_data(email: str, update_data: UserUpdate):
    update_data.date_of_birth = datetime.date.strftime(update_data.date_of_birth, settings.DATE_FORMAT)
    await collection.update_one({'email': email}, {'$set': update_data.model_dump(mode='python')})
    return update_data


async def reset_user_login_unsuccessful_attempts(email: str):
    await collection.update_one({'email': email}, {'$set': {'login_unsuccessful_attempts': 0}})


async def reset_all_login_unsuccessful_attempts():
    cursor = collection.find({})

    async for user in cursor:
        await reset_user_login_unsuccessful_attempts(user['email'])


async def send_emails(birth_month: int):
    emails = []
    users = await _get_users_by_birth_month(birth_month)

    for user in users:
        # TODO: implement email sending
        emails.append({
            'to': user.email,
            'message': f'Hello {user.first_name}, you have 10% discount for this month in example.shop.com"'
        })

    return emails

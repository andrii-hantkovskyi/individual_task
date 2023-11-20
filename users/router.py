from fastapi import APIRouter, HTTPException, Request
from starlette.authentication import UnauthenticatedUser
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK

import settings
from users.models import UserCreate, UserLogin, User, UserUpdate
from users.services import (
    get_user_by_email,
    create_user,
    get_jwt_token,
    update_user_data,
    delete_user_by_email,
    reset_user_login_unsuccessful_attempts
)

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.post('/register', status_code=201)
async def register_user(user_data: UserCreate):
    try:
        await create_user(user_data)
        return Response(status_code=HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@users_router.post('/login')
async def login_user(login_data: UserLogin):
    try:
        return await get_jwt_token(login_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.get('/get-info', response_model=User)
async def get_user(request: Request):
    if isinstance(request.user, UnauthenticatedUser):
        raise HTTPException(status_code=401)
    return await get_user_by_email(request.user['email'])


@users_router.put('/update-info', response_model=User, response_model_exclude={'id'})
async def update_user(request: Request, upd_data: UserUpdate):
    if isinstance(request.user, UnauthenticatedUser):
        raise HTTPException(status_code=401)
    try:
        res = await update_user_data(request.user['email'], upd_data)
        res = res.model_dump(mode='python')
        res['email'] = request.user['email']
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.delete('/delete')
async def delete_user(request: Request):
    await delete_user_by_email(request.user['email'])
    return Response(status_code=HTTP_204_NO_CONTENT)


if settings.DEBUG:
    @users_router.post('/reset-user-login-atts')
    async def res_atts(request: Request):
        if request.headers.get('X-Key') != settings.SECRET_TOKEN:
            raise HTTPException(status_code=403)
        data = await request.json()
        await reset_user_login_unsuccessful_attempts(data['email'])
        return Response(status_code=HTTP_200_OK)

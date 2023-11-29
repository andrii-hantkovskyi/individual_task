from fastapi import APIRouter, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from starlette.authentication import UnauthenticatedUser
from starlette.responses import Response, JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK

import settings
from users.models import UserCreate, UserLogin, User, UserUpdate, RoleTypes, UserInfoAdmin, UserInfoAdvanced, \
    RefreshToken, LoginResponse
from users.services import (
    get_user_by_email,
    create_user,
    login_user,
    update_user_data,
    delete_user_by_email,
    reset_user_login_unsuccessful_attempts, delete_user_by_id, get_user_by_id, send_emails, refresh_jwt_tokens
)

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.post('/register', status_code=201)
async def register_user(user_data: UserCreate):
    try:
        await create_user(user_data)
        return Response(status_code=HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@users_router.post('/login', response_model=LoginResponse)
async def sign_in_user(login_data: UserLogin):
    try:
        return await login_user(login_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.post('/refresh')
async def refresh_tokens(refresh_token: RefreshToken):
    try:
        return await refresh_jwt_tokens(refresh_token.refresh)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.post('/verify', response_model=User)
async def verify_access_token(request: Request):
    if isinstance(request.user, UnauthenticatedUser):
        raise HTTPException(status_code=401)
    return await get_user_by_email(request.user['email'])


@users_router.put('/update-info', response_model=User, response_model_exclude={'id'})
async def update_user(request: Request, upd_data: UserUpdate):
    if isinstance(request.user, UnauthenticatedUser):
        raise HTTPException(status_code=401)
    try:
        res = await update_user_data(request.user['email'], upd_data)
        res['email'] = request.user['email']
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.delete('/delete')
async def delete_user(request: Request):
    await delete_user_by_email(request.user['email'])
    return Response(status_code=HTTP_204_NO_CONTENT)


# Advanced/Admin routes

@users_router.delete('/delete/{user_id}')
async def admin_delete_user(request: Request, user_id: str):
    if isinstance(request.user, UnauthenticatedUser) or request.user['role'] != RoleTypes.admin.value:
        raise HTTPException(status_code=401)

    await delete_user_by_id(user_id)
    return Response(status_code=HTTP_204_NO_CONTENT)


@users_router.get('/get-info/{user_id}')
async def admin_get_user(request: Request, user_id: str):
    if isinstance(request.user, UnauthenticatedUser):
        raise HTTPException(status_code=401)

    match request.user['role']:
        case RoleTypes.admin.value:
            user = await get_user_by_id(user_id)
            json = UserInfoAdmin(**user)
            return JSONResponse(jsonable_encoder(json))
        case RoleTypes.advanced.value:
            user = await get_user_by_id(user_id)
            json = UserInfoAdvanced(**user)
            return JSONResponse(jsonable_encoder(json))
        case _:
            raise HTTPException(status_code=401)


@users_router.post('/send-emails/{birth_month}', status_code=200)
async def admin_send_emails(request: Request, birth_month: int):
    if birth_month > 12 or birth_month < 1:
        raise HTTPException(status_code=400, detail="Month can't be less than 1 and more than 12")

    if (isinstance(request.user, UnauthenticatedUser)
            or request.user['role'] not in [RoleTypes.admin.value, RoleTypes.advanced.value]):
        raise HTTPException(status_code=401)

    res = await send_emails(birth_month)
    return res


if settings.DEBUG:
    @users_router.post('/reset-user-login-atts')
    async def res_atts(request: Request):
        if request.headers.get('X-Key') != settings.SECRET_TOKEN:
            raise HTTPException(status_code=403)
        data = await request.json()
        await reset_user_login_unsuccessful_attempts(data['email'])
        return Response(status_code=HTTP_200_OK)

from typing import List

from fastapi import APIRouter, Request, HTTPException
from starlette.authentication import UnauthenticatedUser
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from orders.models import OrderCreate, Order
from orders.services import get_orders_by_user_id, get_order_by__id_user_id, create_order, delete_order

orders_router = APIRouter(prefix='/orders', tags=['orders'])


@orders_router.get('/', response_model=List[Order])
async def get_user_orders(request: Request):
    if isinstance(request.user, UnauthenticatedUser):
        raise HTTPException(status_code=401)
    res = await get_orders_by_user_id(request.user['_id'])
    return res


@orders_router.get('/{order_id}', response_model=Order)
async def get_user_order(request: Request, order_id: str):
    if isinstance(request.user, UnauthenticatedUser):
        raise HTTPException(status_code=401)
    res = await get_order_by__id_user_id(request.user['_id'], order_id)
    if not res:
        raise HTTPException(status_code=404)
    return res


@orders_router.post('/', response_model=Order, status_code=201)
async def create_user_order(request: Request, order_data: OrderCreate):
    if isinstance(request.user, UnauthenticatedUser):
        raise HTTPException(status_code=401)

    try:
        res = await create_order(request.user['_id'], order_data)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@orders_router.delete('/{order_id}')
async def delete_user_order(request: Request, order_id: str):
    if isinstance(request.user, UnauthenticatedUser):
        raise HTTPException(status_code=401)
    res = await delete_order(request.user['_id'], order_id)
    if res:
        return Response(status_code=HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404)

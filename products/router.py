from typing import List

from fastapi import APIRouter, Request, HTTPException
from starlette.authentication import UnauthenticatedUser
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED

from products.models import Product, ProductCreate, ProductUpdate
from products.services import (
    get_all_products,
    get_all_products_by_type,
    insert_product,
    update_product_info,
    delete_product_by_id, get_product_by_id
)
from users.models import RoleTypes

products_router = APIRouter(prefix='/products', tags=['products'])


@products_router.get('/', response_model=List[Product])
async def get_products():
    return await get_all_products()


@products_router.get('/{product_id}', response_model=Product)
async def get_product(product_id: str):
    res = await get_product_by_id(product_id)
    if not res:
        raise HTTPException(status_code=404)
    return res


@products_router.get('/type/{product_type}', response_model=List[Product])
async def get_products_by_type(product_type: str):
    return await get_all_products_by_type(product_type=product_type)


@products_router.post('/', response_model=Product, status_code=201)
async def create_product(request: Request, product: ProductCreate):
    if isinstance(request.user, UnauthenticatedUser) or request.user.get('role', '') != RoleTypes.admin.value:
        raise HTTPException(status_code=401)

    try:
        res = await insert_product(product)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@products_router.put('/{product_id}', response_model=Product)
async def update_product(request: Request, product_id: str, upd_data: ProductUpdate):
    if isinstance(request.user, UnauthenticatedUser) or request.user.get('role', '') != RoleTypes.admin.value:
        raise HTTPException(status_code=401)

    try:
        res = await update_product_info(product_id, update_data=upd_data)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@products_router.delete('/{product_id}')
async def delete_product(request: Request, product_id: str):
    if isinstance(request.user, UnauthenticatedUser) or request.user.get('role', '') != RoleTypes.admin.value:
        raise HTTPException(status_code=401)

    await delete_product_by_id(product_id)
    return Response(status_code=HTTP_204_NO_CONTENT)

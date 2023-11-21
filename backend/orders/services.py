from bson import ObjectId
from pymongo.results import DeleteResult

from database import database
from orders.models import Order, OrderCreate

collection = database.orders


async def _find_order_by__user_id_product_id(user_id: str, product_id: str):
    return await collection.find_one({'user_id': ObjectId(user_id), 'product_id': ObjectId(product_id)})


async def get_order_by__id_user_id(user_id: str, order_id: str):
    return await collection.find_one({'user_id': ObjectId(user_id), '_id': ObjectId(order_id)})


async def get_orders_by_user_id(user_id: str):
    res = []

    cursor = collection.find({'user_id': ObjectId(user_id)})

    async for order in cursor:
        res.append(Order(**order))

    return res


async def create_order(user_id: str, order_data: OrderCreate):
    order = await _find_order_by__user_id_product_id(user_id, order_data.product_id)
    if order:
        raise ValueError('Order already exists')

    order_data = order_data.model_dump(mode='python')
    order_data['user_id'] = ObjectId(user_id)
    order_data['product_id'] = ObjectId(order_data['product_id'])
    res = await collection.insert_one(order_data)

    return {
        '_id': res.inserted_id,
        **order_data
    }


async def delete_order(user_id: str, order_id: str):
    res: DeleteResult = await collection.delete_one({'user_id': ObjectId(user_id), '_id': ObjectId(order_id)})
    if res.deleted_count > 0:
        return True
    return False

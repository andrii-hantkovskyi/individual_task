from bson import ObjectId

from database import database
from products.models import Product, ProductCreate, ProductUpdate

collection = database.products


async def get_product_by_name(name: str):
    res = await collection.find_one({'name': name})

    return res


async def get_product_by_id(product_id: str):
    res = await collection.find_one({'_id': ObjectId(product_id)})
    return res


async def get_all_products():
    res = []

    cursor = collection.find({})

    async for product in cursor:
        res.append(Product(**product))

    return res


async def get_all_products_by_type(product_type: str):
    res = []

    cursor = collection.find({'type': product_type})

    async for product in cursor:
        res.append(Product(**product))

    return res


async def insert_product(data: ProductCreate):
    product = await get_product_by_name(data.name)
    if product:
        raise ValueError('Product with such name already exists')

    data.type = data.type.value
    res = await collection.insert_one(data.model_dump(mode='python'))
    return {
        '_id': res.inserted_id,
        **data.model_dump(mode='python')
    }


async def update_product_info(product_id: str, update_data: ProductUpdate):
    update_data.type = update_data.type.value

    product = await get_product_by_name(update_data.name)

    if product:
        raise ValueError('Product with such name already exists')

    await collection.update_one({'_id': ObjectId(product_id)}, {'$set': update_data.model_dump(mode='python')})
    return {
        '_id': product_id,
        **update_data.model_dump(mode='python')
    }


async def delete_product_by_id(product_id: str):
    await collection.delete_one({'_id': ObjectId(product_id)})

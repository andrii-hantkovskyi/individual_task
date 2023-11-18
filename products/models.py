from bson import ObjectId
from pydantic import BaseModel


class ProductType(BaseModel):
    _id: str
    name: str


class Product(BaseModel):
    _id: str
    type_id: int
    name: str

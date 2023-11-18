from pydantic import BaseModel


class Order(BaseModel):
    _id: str
    user_id: int
    product_id: int
    qty: int

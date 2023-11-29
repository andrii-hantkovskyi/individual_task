from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, Field

from products.models import Product

PyObjectId = Annotated[str, BeforeValidator(str)]


class OrderBase(BaseModel):
    product: Product
    qty: int = Field(gt=0)


class Order(OrderBase):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')


class OrderCreate(BaseModel):
    product_id: Optional[PyObjectId] = Field(default=None)
    qty: int = Field(gt=0)

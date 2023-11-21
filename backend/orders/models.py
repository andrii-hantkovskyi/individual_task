from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class OrderBase(BaseModel):
    product_id: PyObjectId
    qty: int = Field(gt=0)


class Order(OrderBase):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')


class OrderCreate(OrderBase):
    ...

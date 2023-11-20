from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field, BeforeValidator, ConfigDict

import settings

PyObjectId = Annotated[str, BeforeValidator(str)]

if not settings.DEBUG:
    class ProductTypes(str, Enum):
        phone = 'phone'
        tablet = 'tablet'
        notebook = 'notebook'
        pc = 'pc'
else:
    class ProductTypes(str, Enum):
        phone = 'phone'
        tablet = 'tablet'
        notebook = 'notebook'
        pc = 'pc'
        test = 'test'


class ProductBase(BaseModel):
    type: ProductTypes
    name: str


class Product(ProductBase):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass

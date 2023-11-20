from enum import Enum
from typing import Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict, BeforeValidator

import settings

PyObjectId = Annotated[str, BeforeValidator(str)]

if settings.DEBUG:
    class RoleTypes(str, Enum):
        user = 'user'
        advanced = 'advanced'
        admin = 'admin'
        test = 'test'
else:
    class RoleTypes(str, Enum):
        user = 'user'
        advanced = 'advanced'
        admin = 'admin'


class UserBase(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    delivery_address: str
    phone_number: int = Field(gt=380000000000, lt=380999999999)


class UserCreateBase(UserBase):
    email: str
    role: RoleTypes


class User(UserBase):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    email: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class UserUpdate(UserBase):
    ...


class UserJWT(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias='_id')
    email: str
    role: RoleTypes
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class UserCreate(UserCreateBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str

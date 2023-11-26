import datetime
from enum import Enum
from typing import Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict, BeforeValidator, field_validator

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
    date_of_birth: datetime.date
    phone_number: int = Field(gt=380000000000, lt=380999999999)

    @classmethod
    @field_validator('date_of_birth', mode='before')
    def check_date_of_birth(cls, value):
        return datetime.datetime.strptime(value, settings.DATE_FORMAT).date()


class UserCreateBase(UserBase):
    email: str


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
    user_id: Optional[PyObjectId] = Field(default=None, alias='_id')
    email: str
    role: RoleTypes
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class UserCreate(UserCreateBase):
    password: str
    role: RoleTypes = RoleTypes.user


class UserLogin(BaseModel):
    email: str
    password: str


class UserInfoAdmin(User):
    role: str


class UserInfoAdvanced(BaseModel):
    first_name: str
    email: str


class RefreshToken(BaseModel):
    refresh: str

from pydantic import BaseModel, Field


class Role(BaseModel):
    _id: str
    name: str


class UserBase(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    delivery_address: str
    phone_number: int = Field(gt=380000000000, lt=380999999999)
    email: str
    role_id: int


class User(UserBase):
    _id: str


class UserJWT(BaseModel):
    _id: str
    email: str
    role_id: int


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str

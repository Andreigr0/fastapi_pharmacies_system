from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    email: str
    login: str = Field()


class UserCreate(UserBase):
    password: str


class UserWithoutItems(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserBase):
    from items.schemas import ItemWithoutOwnerId

    id: int
    is_active: bool
    items: list[ItemWithoutOwnerId] = []

    class Config:
        orm_mode = True

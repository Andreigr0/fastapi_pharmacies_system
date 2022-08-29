from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemWithoutOwnerId(ItemBase):
    id: int

    class Config:
        orm_mode = True


class Item(ItemBase):
    from users.schemas import UserWithoutItems

    id: int
    owner_id: int
    owner: UserWithoutItems

    class Config:
        orm_mode = True

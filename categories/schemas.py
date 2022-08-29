from pydantic import BaseModel


class CategoryBase(BaseModel):
    title: str
    subcategories: list['CategoryBase']


class Category(CategoryBase):
    id: int
    subcategories: list['Category']

    class Config:
        orm_mode = True

import inspect
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
from typing import Any, Type

from fastapi import UploadFile
from fastapi.params import Query, Depends, Form, File
from pydantic import BaseModel
from pydantic.fields import Field, ModelField
from pydantic.utils import GetterDict

from pharmacies.schemas import Pharmacy


class FilterItem(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class ProductOfferType(str, Enum):
    add_bonuses = 'add_bonuses'
    minus_percent = 'minus_percent'


class ProductOffer(BaseModel):
    value: int
    type: ProductOfferType


class ProductBase(BaseModel):
    title: str
    description: str
    archived: bool = False


class ProductCreate(ProductBase):
    pharmacy_id: int
    price: float
    count: int
    image: UploadFile

    @classmethod
    def as_form(cls,
                image: UploadFile = File(...),
                pharmacy_id: int = Form(..., ge=1, description='Id аптеки'),
                price: float = Form(..., ge=0),
                count: int = Form(..., ge=0),
                ):
        return cls(pharmacy_id=pharmacy_id, price=price, count=count, image=image)


class Product(ProductBase):
    id: int
    image: str | None
    min_price: float | None
    price: float | None
    offer: ProductOffer | None
    form: FilterItem | None
    amount_in_package: int | None
    dosage: FilterItem | None


class ProductListGetter(GetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        if key == 'dosage':
            return self._obj.dosage.title
        if key == 'form':
            return self._obj.form.title
        return super().get(key, default)


class ProductListItem(Product):
    # combine these three
    form: str
    amount_in_package: int | None
    dosage: str | None

    class Config:
        orm_mode = True
        getter_dict = ProductListGetter


class ProductDetails(Product):
    images: list[str]
    description: str | None
    in_stock_count: int | None
    manufacturer: FilterItem | None = Field(default=None, description='Производитель')
    country: FilterItem | None
    by_prescription: bool = False
    active_substances: list[FilterItem] = []
    color_taste_aroma: str | None = None
    expiration: timedelta | None
    storage_conditions: str | None
    indications_for_use: str | None
    contraindications: str | None
    pharmacological_effect: str | None

    pharmacies: list[Pharmacy] = []
    similar: list[Product] = []
    analogues: list[Product] = []

    class Config:
        orm_mode = True


class ProductSort(str, Enum):
    """Сортировка товаров"""

    by_popularity = 'by_popularity'
    cheap_first = 'cheap_first'
    expensive_first = 'expensive_first'
    by_name_asc = 'by_name_asc'


@dataclass
class ProductQuery:
    sort: ProductSort = Query(default=ProductSort.by_popularity, description='Сортировка')
    category: list[int] | None = Query(default=None, description='Категории')
    in_stock: bool = Query(default=True, description='В наличии')
    in_favorite_pharmacies: bool = Query(default=False, description='В любимых аптеках')
    in_offers: bool = Query(default=False, description='Товары по акции')
    by_prescription: bool = Query(default=False, description='Отпуск по рецепту')
    min_price: int = Query(default=0, description='Минимальная цена')
    max_price: int = Query(default=None, description='Максимальная цена')
    brand: list[int] | None = Query(default=None, description='Бренд')
    form: list[int] | None = Query(default=None, description='Лекарственная форма')
    mnn: list[int] | None = Query(default=None, description='Действующее вещество')
    dosage: list[int] | None = Query(default=None, description='Дозировка')
    amount: list[int] | None = Query(default=None, description='Количество в упаковке')
    producer: list[int] | None = Query(default=None, description='Производитель')
    country: list[int] | None = Query(default=None, description='Страна производства')

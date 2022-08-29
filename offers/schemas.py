from datetime import datetime

from pydantic import BaseModel, Field

from pharmacies.schemas import Pharmacy
from products.schemas import Product, FilterItem


class Offer(BaseModel):
    id: int
    image: str
    from_date: datetime
    to_date: datetime


class OfferDetails(Offer):
    category: FilterItem
    subcategory: FilterItem | None = Field(default=None, description='Подкатегория')
    terms: str
    products: list[Product]
    pharmacies: list[Pharmacy]

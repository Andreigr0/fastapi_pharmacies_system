from pydantic import BaseModel


class PharmacyCreate(BaseModel):
    title: str
    latitude: float
    longitude: float
    address: str


class Pharmacy(PharmacyCreate):
    id: int

    class Config:
        orm_mode = True

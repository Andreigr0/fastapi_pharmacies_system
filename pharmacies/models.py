from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from products.models import ProductsPharmaciesModel
from users.models import UserModel


class PharmacyModel(Base):
    __tablename__ = "pharmacies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    products: ProductsPharmaciesModel = relationship("ProductsPharmaciesModel",
                                                     back_populates="pharmacy")
    in_favorites: list['FavoritePharmaciesModel'] = relationship('FavoritePharmaciesModel', back_populates="pharmacy")


class FavoritePharmaciesModel(Base):
    __tablename__ = "favorite_pharmacies"

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    pharmacy_id = Column(Integer, ForeignKey('pharmacies.id'), primary_key=True)

    user: UserModel = relationship("UserModel", back_populates="favorite_pharmacies")
    pharmacy: PharmacyModel = relationship("PharmacyModel", back_populates='in_favorites')

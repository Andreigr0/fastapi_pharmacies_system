from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship

from app.database import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    first_name = Column(String, nullable=True)
    birth_date = Column(TIMESTAMP, nullable=True)

    items = relationship('ItemModel', back_populates='owner')
    favorite_pharmacies: list['pharmacies.models.FavoritePharmaciesModel'] = \
        relationship('FavoritePharmaciesModel', back_populates='user')

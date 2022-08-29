from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class CategoryModel(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    parent = relationship('CategoryModel', remote_side=[id])
    children: list['CategoryModel'] = relationship('CategoryModel', back_populates='parent')

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, select, func, and_, TIMESTAMP
from sqlalchemy.orm import relationship, column_property, declarative_mixin, declared_attr, backref

from app.database import Base


@declarative_mixin
class FilterModelMixin:
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    @declared_attr
    def products(cls):
        return relationship('ProductModel', cascade="all, delete")


class BrandModel(Base, FilterModelMixin):
    __tablename__ = 'brands'


class FormModel(Base, FilterModelMixin):
    __tablename__ = 'forms'


class ActiveSubstanceModel(Base):
    __tablename__ = 'active_substances'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    products: list['categories.models.ProductModel'] = relationship('ActiveSubstancesProductsModel',
                                                                    back_populates='substance')


class DosageModel(Base, FilterModelMixin):
    __tablename__ = 'dosages'


class ManufacturerModel(Base, FilterModelMixin):
    __tablename__ = 'manufacturers'


class CountryModel(Base, FilterModelMixin):
    __tablename__ = 'countries'


class ProductImageModel(Base):
    __tablename__ = 'product_images'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)

    product = relationship('ProductModel', back_populates='images')


class ActiveSubstancesProductsModel(Base):
    __tablename__ = 'active_substances_products'

    substance_id = Column(ForeignKey('active_substances.id'), primary_key=True)
    product_id = Column(ForeignKey('products.id'), primary_key=True)

    product: 'ProductModel' = relationship('ProductModel', back_populates='active_substances')
    substance: ActiveSubstanceModel = relationship('ActiveSubstanceModel', back_populates='products')


class ProductsPharmaciesModel(Base):
    __tablename__ = "products_pharmacies"

    product_id = Column(ForeignKey('products.id'), primary_key=True)
    pharmacy_id = Column(ForeignKey('pharmacies.id'), primary_key=True)
    price = Column(Float, nullable=True)
    in_stock_count = Column(Integer, nullable=False, default=0)

    product: 'ProductModel' = relationship("ProductModel", back_populates="pharmacies", cascade='all, delete')
    pharmacy: 'pharmacies.models.PharmacyModel' = relationship("PharmacyModel", back_populates="products")


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    archived = Column(Boolean, nullable=False, default=False)
    description = Column(String, nullable=False)
    amount_in_package = Column(Integer, nullable=True)
    by_prescription = Column(Boolean, nullable=False, default=False)
    expiration = Column(TIMESTAMP)
    storage_conditions = Column(String)
    color_taste_aroma = Column(String)
    indications_for_use = Column(String)
    contraindications = Column(String)
    pharmacological_effect = Column(String)

    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand: BrandModel = relationship(BrandModel, back_populates='products')

    form_id = Column(Integer, ForeignKey('forms.id'))
    form: FormModel = relationship(FormModel, back_populates='products')

    dosage_id = Column(Integer, ForeignKey('dosages.id'), nullable=True)
    dosage: DosageModel = relationship(DosageModel, back_populates='products')

    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'))
    manufacturer = relationship(ManufacturerModel, back_populates='products')

    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship(CountryModel, back_populates='products')

    images: list[ProductImageModel] = relationship('ProductImageModel', back_populates='product', cascade='all, delete')
    pharmacies: list['pharmacies.models.PharmacyModel'] = relationship("ProductsPharmaciesModel",
                                                                       back_populates="product", cascade='all, delete')
    active_substances: list[ActiveSubstanceModel] = relationship("ActiveSubstancesProductsModel",
                                                                 back_populates='product')

    min_price: float = column_property(
        select(func.min(ProductsPharmaciesModel.price))
        .group_by(ProductsPharmaciesModel.product_id)
        .where(and_(ProductsPharmaciesModel.product_id == id))
        .scalar_subquery()
    )

    price: float = column_property(
        select(func.max(ProductsPharmaciesModel.price))
        .group_by(ProductsPharmaciesModel.product_id)
        .where(and_(ProductsPharmaciesModel.product_id == id))
        .scalar_subquery()
    )

import random

import pytest

from pharmacies.models import PharmacyModel
from products.models import *


def test_create_filter_models(db_test, test_creation, faker):
    test_creation(BrandModel(title='Brand 1'))
    test_creation(FormModel(title='Form 1'))
    test_creation(DosageModel(title='Dosage 1'))
    test_creation(ManufacturerModel(title=faker.company()))
    test_creation(CountryModel(title='Country 1'))


def test_create_product(db_test, test_creation, faker):
    product = ProductModel(title='Product 1', description='Desc 1')
    product.dosage = db_test.query(DosageModel).first()
    test_creation(product)
    assert product.dosage.id == 1


def test_create_image(db_test):
    product: ProductModel = db_test.query(ProductModel).first()
    image = ProductImageModel(url='image')
    product.images.append(image)
    assert product.images[0].url == 'image'


@pytest.mark.parametrize(
    'product', [
        ProductModel(title='First prod', description='First desc'),
        ProductModel(title='Second prod', description='Second desc'),
        ProductModel(title='Third prod', description='Third desc'),
    ],
)
@pytest.mark.parametrize(
    'pharmacy', [
        PharmacyModel(title='First Pharmacy', address='Address first', latitude=1.11, longitude=1.12),
        PharmacyModel(title='Second Pharmacy', address='Address 2', latitude=2.22, longitude=2.23),
    ],
)
def test_create_product_pharmacy(db_test, product, pharmacy):
    association = ProductsPharmaciesModel(price=round(random.uniform(1, 200), 2), in_stock_count=random.randint(1, 200))
    association.pharmacy = pharmacy
    product.pharmacies.append(association)
    db_test.add(association)
    db_test.commit()
    assert association.product_id == product.id, association.pharmacy_id == pharmacy.id


def test_delete_dosage_and_related_products(db_test):
    dosage: DosageModel = db_test.query(DosageModel).first()
    db_test.delete(dosage)
    db_test.commit()
    products: list[ProductModel] = db_test.query(ProductModel).filter(ProductModel.dosage_id == dosage.id).all()
    assert not products

import aiofiles
from fastapi import UploadFile
from sqlalchemy.orm import Session

from pharmacies.models import PharmacyModel
from products.models import ProductsPharmaciesModel, ProductModel, ProductImageModel
from products.schemas import ProductCreate


async def create_file(file: UploadFile):
    path = f'files/{file.filename}'
    async with aiofiles.open(path, 'wb+') as out_file:
        content = await file.read()
        await out_file.write(content)

    return {
        'filename': file.filename,
        'path': path
    }


def get_pharmacy(db: Session, pharmacy_id: int):
    return db.query(PharmacyModel).filter_by(id=pharmacy_id).first()


def create_product(body: ProductCreate, db: Session, pharmacy: PharmacyModel, image_url: str):
    assoc = ProductsPharmaciesModel(price=body.price, in_stock_count=body.count)
    assoc.pharmacy = pharmacy

    product = ProductModel(title=body.title, description=body.description, archived=body.archived)
    product.pharmacies.append(assoc)

    if image_url:
        product.images.append(ProductImageModel(url=image_url))

    db.add(product)
    db.commit()
    return product

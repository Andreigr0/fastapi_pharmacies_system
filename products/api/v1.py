from fastapi import APIRouter, HTTPException
from fastapi import status
from fastapi.params import Path, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.tags import Tags
from products import crud
from products.models import ProductModel
from products.schemas import Product, ProductQuery, ProductDetails, ProductListItem, ProductCreate

router = APIRouter(
    tags=[Tags.products],
    prefix='/products',
)


@router.get('', response_model=list[ProductListItem])
def get_products(query: ProductQuery = Depends(), db: Session = Depends(get_db)):
    db_req = db.query(ProductModel)
    products: list[ProductModel] = db_req.all()
    return products


@router.post('', response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(body: ProductCreate = Depends(ProductCreate.as_form), db: Session = Depends(get_db)):
    pharmacy = crud.get_pharmacy(db, body.pharmacy_id)
    if not pharmacy:
        raise HTTPException(status_code=400, detail='No such pharmacy')

    image_url = None
    if body.image:
        image_url = await crud.create_file(body.image)
    return crud.create_product(body, db, pharmacy, image_url)


@router.get('/{id}', response_model=ProductDetails)
def get_product_by_id(id: int = Path(), db: Session = Depends(get_db)):
    return db.query(ProductModel).filter_by(id=id).first()


@router.post('/{id}/favorite', tags=[Tags.favorites])
def add_product_to_favorites(id: int = Path()):
    return None


@router.delete('/{id}/favorite', tags=[Tags.favorites])
def remove_product_from_favorites(id: int = Path()):
    return None

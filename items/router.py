from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from items import schemas, crud

router = APIRouter(
    prefix='/items',
    tags=['items'],
)


@router.get('', response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip, limit)


@router.put('/{item_id}')
def update_item(item_id: int, item: schemas.Item):
    return item.dict()
    # return {'item_name': item.title, 'item_id': item_id}


@router.post('')
async def create_item(item: schemas.Item):
    return item.dict()

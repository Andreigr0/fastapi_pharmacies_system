from fastapi import APIRouter

from categories.schemas import Category

router = APIRouter(
    tags=['categories'],
    prefix='/categories'
)


@router.get('', response_model=list[Category])
def get_categories():
    return []


@router.get('/{id}', response_model=Category)
def get_category_by_id(id: int):
    return None

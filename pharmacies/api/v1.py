from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.database import get_db
from app.tags import Tags
from pharmacies import crud
from pharmacies.models import PharmacyModel
from pharmacies.schemas import Pharmacy, PharmacyCreate
from users.api.v1 import get_current_user
from users.models import UserModel

router = APIRouter(
    prefix='/pharmacies',
    tags=[Tags.pharmacies],
)


@router.get('', response_model=list[Pharmacy])
def get_pharmacies(db: Session = Depends(get_db)):
    return crud.get_pharmacies(db)


@router.post('', response_model=Pharmacy, status_code=status.HTTP_201_CREATED)
def create_pharmacy(body: PharmacyCreate, db: Session = Depends(get_db)):
    return crud.create_pharmacy(body, db)


@router.get('/favorites', tags=[Tags.favorites])
def get_favorite_pharmacies(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail='Not authorized')

    return crud.get_favorite_pharmacies(current_user.id, db)


def verify_pharmacy(pharmacy_id: int, db: Session = Depends(get_db)) -> PharmacyModel:
    pharmacy = crud.get_pharmacy_by_id(pharmacy_id, db)
    if not pharmacy:
        raise HTTPException(status_code=404, detail='Pharmacy not found')
    return pharmacy


@router.get('/{pharmacy_id}', response_model=Pharmacy)
def get_pharmacy(pharmacy: PharmacyModel = Depends(verify_pharmacy)):
    return pharmacy


@router.post('/{pharmacy_id}/favorite', tags=[Tags.favorites], status_code=status.HTTP_201_CREATED)
def add_pharmacy_to_favorites(
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user),
        pharmacy: PharmacyModel = Depends(verify_pharmacy),
):
    in_favorites = crud.get_favorite_pharmacy(pharmacy.id, current_user.id, db)
    if not in_favorites:
        crud.add_to_favorites(pharmacy, current_user, db)

    return {'result': True}


@router.delete('/{pharmacy_id}/favorite', tags=[Tags.favorites], status_code=status.HTTP_204_NO_CONTENT)
def remove_pharmacy_from_favorites(
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user),
        pharmacy: PharmacyModel = Depends(verify_pharmacy),
):
    in_favorites = crud.get_favorite_pharmacy(pharmacy.id, current_user.id, db)
    if in_favorites:
        crud.remove_from_favorites(pharmacy, current_user, db)

    return {'result': True}

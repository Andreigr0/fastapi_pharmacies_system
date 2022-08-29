from sqlalchemy.orm import Session

from pharmacies.models import PharmacyModel, FavoritePharmaciesModel
from pharmacies.schemas import PharmacyCreate
from users.models import UserModel


def get_pharmacies(db: Session) -> list[PharmacyModel]:
    return db.query(PharmacyModel).all()


def get_pharmacy_by_id(pharmacy_id: int, db: Session) -> PharmacyModel | None:
    return db.query(PharmacyModel).filter_by(id=pharmacy_id).first()


def get_favorite_pharmacy(pharmacy_id: int, user_id: int, db: Session) -> FavoritePharmaciesModel | None:
    return db.query(FavoritePharmaciesModel).filter_by(pharmacy_id=pharmacy_id, user_id=user_id).first()


def get_favorite_pharmacies(user_id: int, db: Session):
    fav = FavoritePharmaciesModel
    return db.query(PharmacyModel).join(fav).filter(fav.user_id == user_id).all()


def create_pharmacy(body: PharmacyCreate, db: Session) -> PharmacyModel:
    pharmacy = PharmacyModel(title=body.title,
                             address=body.address,
                             latitude=body.latitude,
                             longitude=body.longitude)
    db.add(pharmacy)
    db.commit()
    return pharmacy


def add_to_favorites(pharmacy: PharmacyModel, user: UserModel, db: Session):
    favorite = FavoritePharmaciesModel()
    favorite.pharmacy = pharmacy
    user.favorite_pharmacies.append(favorite)
    db.add(favorite)
    db.commit()
    return favorite


def remove_from_favorites(pharmacy: PharmacyModel, user: UserModel, db: Session):
    favorite = get_favorite_pharmacy(pharmacy.id, user.id, db)
    db.delete(favorite)
    db.commit()
    return pharmacy

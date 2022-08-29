from pharmacies.models import PharmacyModel, FavoritePharmaciesModel
from users.models import UserModel


def test_create_pharmacy(db_test):
    pharmacy = PharmacyModel(title='Title', address='address', latitude=52.6, longitude=39.6)
    db_test.add(pharmacy)
    db_test.commit()
    assert pharmacy.id


def test_add_to_favorites(db_test, faker):
    pharmacy = PharmacyModel(title='Title', address='address', latitude=10, longitude=10)
    user = UserModel(email=faker.email(), login=faker.user_name(), hashed_password='password')
    favorite = FavoritePharmaciesModel()
    favorite.pharmacy = pharmacy
    user.favorite_pharmacies.append(favorite)
    db_test.add(favorite)
    db_test.commit()

    assert pharmacy.in_favorites
    assert user.favorite_pharmacies

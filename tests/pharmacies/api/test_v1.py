import pytest

from pharmacies.models import FavoritePharmaciesModel
from users.models import UserModel


@pytest.mark.anyio
async def test_delay():
    print('test 🧐')


@pytest.mark.anyio
async def test_add_to_favorite(test_client, bearer_header, create_pharmacy, current_user: UserModel, db_test):
    pharmacy = create_pharmacy
    response = test_client.post(f'/pharmacies/{pharmacy.id}/favorite', headers=bearer_header)

    assert response.status_code == 201
    assert response.json() == {'result': True}
    favorites = db_test.query(FavoritePharmaciesModel).filter_by(user_id=current_user.id).all()
    print(favorites)

# def test_remove_from_favorite(test_client, bearer, create_pharmacy):
#     response = test_client.post(f'/pharmacies/{create_pharmacy.id}/favorite', headers=bearer)

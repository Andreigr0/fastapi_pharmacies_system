import pytest

from app.services.get_current_user import get_current_user
from pharmacies import crud
from pharmacies.schemas import PharmacyCreate
from users.models import UserModel


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
def bearer(test_client):
    email = 'test@test.com'
    password = 'password'

    auth = test_client.post('/token', data={'username': email, 'password': password})
    bearer = auth.json()['access_token']
    return bearer


@pytest.fixture
def bearer_header(bearer):
    return {'Authorization': f'Bearer {bearer}'}


@pytest.fixture
def create_pharmacy(db_test):
    body = PharmacyCreate(title='Pharmacy', latitude=1, longitude=2, address='Address')
    return crud.create_pharmacy(body, db_test)


@pytest.fixture
async def current_user(bearer, db_test) -> UserModel:
    return await get_current_user(bearer, db_test)

from datetime import timedelta

from fastapi import status

from users.auth_utils import create_access_token
from users.schemas import UserCreate


def test_create_user(client):
    user = UserCreate(email='wrong', login='login', password='password')
    response = client.post(url='/users', json=user.dict())
    data: dict = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert data['email'] == 'wrong'
    assert data['login'] == 'login'
    assert 'password' not in data
    assert 'id' in data


def test_current_user_not_logged_in(client):
    response = client.get('/users/me')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_not_existing_current_user(client):
    access_token = create_access_token(data={'sub': 'user.email'}, expires_delta=timedelta(minutes=15))
    response = client.get('/users/me', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_existing_current_user_logged_in(client):
    user = UserCreate(email='wrong', login='login', password='password')
    client.post(url='/users', json=user.dict())

    access_token = create_access_token(data={'sub': 'wrong'}, expires_delta=timedelta(minutes=15))
    response = client.get('/users/me', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == status.HTTP_200_OK

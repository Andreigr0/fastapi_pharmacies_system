from pharmacies.schemas import PharmacyCreate


def test_create_pharmacy(client):
    body = PharmacyCreate(title='Title', latitude=52.6, longitude=39.6, address='address')
    response = client.post('/pharmacies', json=(body.dict()))
    data: dict = response.json()
    assert response.status_code == 201

    assert data['title'] == 'Title'
    assert data['latitude'] == 52.6
    assert data['longitude'] == 39.6
    assert data['address'] == 'address'

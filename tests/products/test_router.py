from products.schemas import ProductCreate


def test_create_product(client):
    product = ProductCreate(title='Test product', description='Test description', image='image_url', pharmacy_id=1,
                            price=39.65, archived=False)
    response = client.post('/products', json=product.dict())
    assert response.status_code == 201


def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200

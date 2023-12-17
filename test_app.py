import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_to_cart(client):
    response = client.post('/add_to_cart', json={"item": "Product A", "price": 1000})
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert "message" in data
    assert "cart" in data
    assert "total_purchase_amount" in data
    assert "discount_code" in data

def test_checkout_without_discount(client):
    response = client.post('/checkout', json={"discount_code": None})
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert "message" in data
    assert "total_discount_amount" in data
    assert "total_purchase_amount" in data

def test_checkout_with_discount(client):
    # Add an item to the cart
    client.post('/add_to_cart', json={"item": "Product A", "price": 1000})

    # Checkout with a discount code
    response = client.post('/checkout', json={"discount_code": "DISCOUNT_1"})
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert "message" in data
    assert "total_discount_amount" in data
    assert "total_purchase_amount" in data

def test_generate_discount_code(client):
    response = client.post('/admin/generate_discount_code')
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert "message" in data
    assert "discount_code" in data

def test_purchase_details(client):
    response = client.get('/admin/purchase_details')
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert "item_count" in data
    assert "total_purchase_amount" in data
    assert "discount_codes" in data
    assert "total_discount_amount" in data

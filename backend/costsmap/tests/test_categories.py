import asyncio

from .main import client, clean_testing
from ..project.models import database


def test_create_category():
    clean_testing()
    with client:
        response = client.post('/api/v1/auth/registration/', json={
            "email": "someone@gmail.com",
            "password1": "Password123",
            "password2": "Password123",
            "currency": "$",
        })
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.post('/api/v1/categories/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "title": "some category",
            "color": "#333333"
        })
        assert response.status_code == 201
        assert response.json() == {
            "title": "some category",
            "costs_limit": None,
            "color": "#333333",
            "costs_sum": 0.0,
            "id": 1
        }


def test_create_category_with_costs_limit():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.post('/api/v1/categories/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "title": "some category1",
            "costs_limit": 500,
            "color": "#333333",
        })
        assert response.status_code == 201
        assert response.json() == {
            "title": "some category1",
            "costs_limit": 500,
            "color": "#333333",
            "costs_sum": 0.0,
            "id": 2
        }


def test_create_category_with_already_exists_title():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.post('/api/v1/categories/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "title": "some category",
            "costs_limit": 500,
            "color": "#333333",
        })
        assert response.status_code == 400


def test_get_all_categories():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.get('/api/v1/categories/', headers={
            "Authorization": f"Bearer {token}"
        })
        print(response.json())
        assert response.status_code == 200
        assert response.json() == [{
            "title": "some category",
            "costs_limit": None,
            "color": "#333333",
            "costs_sum": 0.0,
            "id": 1
        }, {
            "title": "some category1",
            "costs_limit": 500,
            "color": "#333333",
            "costs_sum": 0.0,
            "id": 2
        }]


def test_get_all_categories_with_costs():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        asyncio.run(_create_testing_cost())
        response = client.get('/api/v1/categories/', headers={
            "Authorization": f"Bearer {token}"
        })
        print(response.json())
        assert response.status_code == 200
        assert response.json() == [{
            "title": "some category",
            "costs_limit": None,
            "color": "#333333",
            "costs_sum": 500.0,
            "id": 1
        }, {
            "title": "some category1",
            "costs_limit": 500,
            "color": "#333333",
            "costs_sum": 0.0,
            "id": 2
        }]


async def _create_testing_cost():
    create_card_query = "insert into cards (title, currency, color, amount, user) values ('smth', '$', '#333333', 1000, 1)"
    await database.execute(create_card_query)
    query = "insert into costs (user_currency_amount, category, card, user, date) values(500, 1, 1, 1, date('now'))"
    await database.execute(query)


def test_get_concrete_category():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.get('/api/v1/categories/1/', headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 200
        assert response.json() == {
            "title": "some category",
            "costs_limit": None,
            "color": "#333333",
            "costs_sum": 0.0,
            "id": 1
        }


def test_get_concrete_category_with_doesnt_exist_id():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.get('/api/v1/categories/4/', headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 404


def test_update_concrete_category():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.put('/api/v1/categories/1/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "title": "new category",
            "costs_limit": 1000,
            "color": "#333333",
        })
        assert response.status_code == 200
        assert response.json() == {
            "title": "new category",
            "costs_limit": 1000,
            "color": "#333333",
            "costs_sum": 0.0,
            "id": 1
        }


def test_update_concrete_category_with_already_exists_title():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.put('/api/v1/categories/1/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "title": "some category1",
            "costs_limit": 1000,
            "color": "#333333",
        })
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Category with this title already exists"
        }


def test_update_with_doesnt_exist_category_id():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.put('/api/v1/categories/4/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "title": "some category1",
            "costs_limit": 1000,
            "color": "#333333",
        })
        assert response.status_code == 404


def test_delete_category():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.delete('/api/v1/categories/1/', headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 204


def test_delete_category_with_doesnt_exist_category_id():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.delete('/api/v1/categories/4/', headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 404

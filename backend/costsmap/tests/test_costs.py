import asyncio
from datetime import date

from dateutil.relativedelta import relativedelta

from .main import client, clean_testing
from ..project.models import database


def test_create_new_cost():
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
        category = _create_category(token)
        card = _create_card(token)
        asyncio.run(_add_card_amount())
        response = client.post('/api/v1/costs/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "user_currency_amount": 100,
            "card_id": card['id'],
            "category_id": category['id']
        })
        assert response.status_code == 201
        cost_json = response.json()
        assert "id" in cost_json
        assert cost_json['user_currency_amount'] == 100
        assert cost_json['card_currency_amount'] is None
        assert cost_json['date'] == date.today().isoformat()
        assert cost_json['card']['title'] == card['title']
        assert cost_json['category']['title'] == category['title']


def _create_category(token: str):
    response = client.post('/api/v1/categories/', headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "title": "Category1",
        "color": "#ff0000"
    })
    assert response.status_code == 201
    created_category = response.json()
    return created_category


def _create_card(token: str):
    response = client.post('/api/v1/cards/', headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "title": "Card1",
        "currency": "$",
        "color": "#000000"
    })
    assert response.status_code == 201
    created_card = response.json()
    return created_card


async def _add_card_amount():
    query = "update cards set amount = 1000"
    await database.execute(query)


def test_create_cost_with_card_currency():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        card = _create_card_with_differrent_currency(token)
        asyncio.run(_add_card_with_differrent_currency_amount(card['id']))
        response = client.post('/api/v1/costs/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "user_currency_amount": 100,
            "card_currency_amount": 5000,
            "card_id": card['id'],
            "category_id": 1
        })
        assert response.status_code == 201
        cost_json = response.json()
        assert "id" in cost_json
        assert cost_json['user_currency_amount'] == 100
        assert cost_json['card_currency_amount'] == 5000
        assert cost_json['date'] == date.today().isoformat()
        assert cost_json['card']['title'] == card['title']
        assert cost_json['category']['id'] == 1


def test_create_cost_for_card_with_differrent_currency_and_without_card_currency_amount_field():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.post('/api/v1/costs/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "user_currency_amount": 100,
            "card_id": 2,
            "category_id": 1
        })
        assert response.status_code == 400
        cost_json = response.json()
        assert cost_json['detail'] == "Cost for card with differrent currency than default must contain `card_currency_amount` field"


def _create_card_with_differrent_currency(token: str):
    response = client.post('/api/v1/cards/', headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "title": "Card2",
        "currency": "₽",
        "color": "#000000"
    })
    assert response.status_code == 201
    created_card = response.json()
    return created_card


async def _add_card_with_differrent_currency_amount(card_id):
    query = "update cards set amount = 10000 where id = :card_id"
    await database.execute(query, values={'card_id': card_id})


def test_create_cost_with_date():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        previous_month = (date.today() - relativedelta(months=1)).isoformat()
        response = client.post('/api/v1/costs/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "user_currency_amount": 100,
            "card_id": 1,
            "category_id": 1,
            "date": previous_month
        })
        assert response.status_code == 201
        cost_json = response.json()
        assert "id" in cost_json
        assert cost_json['user_currency_amount'] == 100
        assert cost_json['card_currency_amount'] is None
        assert cost_json['date'] == previous_month
        assert cost_json['card']['id'] == 1
        assert cost_json['category']['id'] == 1


def test_create_cost_with_amount_more_than_card_amount():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        previous_month = (date.today() - relativedelta(months=1)).isoformat()
        response = client.post('/api/v1/costs/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "user_currency_amount": 500000,
            "card_id": 1,
            "category_id": 1,
            "date": previous_month
        })
        assert response.status_code == 400
        cost_json = response.json()
        assert cost_json['detail'] == 'Cost amount is more than card amount'


def test_get_all_costs():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.get('/api/v1/costs/', headers={
            "Authorization": f"Bearer {token}"
        })
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) == 2


def test_get_all_costs_for_previous_month():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        previous_month = (date.today() - relativedelta(months=1)).isoformat()[:-3]
        response = client.get(f'/api/v1/costs/?month={previous_month}', headers={
            "Authorization": f"Bearer {token}"
        })
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) == 1


def test_get_all_costs_for_next_month():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        next_month = (date.today() + relativedelta(months=1)).isoformat()[:-3]
        response = client.get(f'/api/v1/costs/?month={next_month}', headers={
            "Authorization": f"Bearer {token}"
        })
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) == 0


def test_delete_cost():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.delete(f'/api/v1/costs/1/', headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 204


def test_delete_doesnt_exist_cost():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.delete(f'/api/v1/costs/10/', headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 404

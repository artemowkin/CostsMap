import asyncio
from datetime import date

from dateutil.relativedelta import relativedelta

from .main import client, clean_testing
from ..project.models import database


def test_create_new_income():
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
        card = _create_card(token)
        asyncio.run(_add_card_amount())
        response = client.post('/api/v1/incomes/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "userCurrencyAmount": 100,
            "cardId": card['id'],
        })
        assert response.status_code == 201
        income_json = response.json()
        assert "id" in income_json
        assert income_json['userCurrencyAmount'] == 100
        assert income_json['cardCurrencyAmount'] is None
        assert income_json['date'] == date.today().isoformat()
        assert income_json['card']['title'] == card['title']


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


def test_create_income_with_card_currency():
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
        response = client.post('/api/v1/incomes/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "userCurrencyAmount": 100,
            "cardCurrencyAmount": 5000,
            "cardId": card['id'],
        })
        assert response.status_code == 201
        income_json = response.json()
        assert "id" in income_json
        assert income_json['userCurrencyAmount'] == 100
        assert income_json['cardCurrencyAmount'] == 5000
        assert income_json['date'] == date.today().isoformat()
        assert income_json['card']['title'] == card['title']


def test_create_income_for_card_with_differrent_currency_and_without_card_currency_amount_field():
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
        response = client.post('/api/v1/incomes/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "user_currency_amount": 100,
            "cardId": 2,
            "categoryId": 1
        })
        assert response.status_code == 400
        income_json = response.json()
        assert income_json['detail'] == "Income for card with differrent currency than default must contain `card_currency_amount` field"


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


def test_create_income_with_date():
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
        response = client.post('/api/v1/incomes/', headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "userCurrencyAmount": 100,
            "cardId": 1,
            "date": previous_month
        })
        assert response.status_code == 201
        income_json = response.json()
        assert "id" in income_json
        assert income_json['userCurrencyAmount'] == 100
        assert income_json['cardCurrencyAmount'] is None
        assert income_json['date'] == previous_month
        assert income_json['card']['id'] == 1


def test_get_all_incomes():
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
        response = client.get('/api/v1/incomes/', headers={
            "Authorization": f"Bearer {token}"
        })
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) == 2


def test_get_total_incomes():
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
        response = client.get('/api/v1/incomes/total/', headers={
            "Authorization": f"Bearer {token}"
        })
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['totalIncomes'] == 200


def test_get_all_incomes_for_previous_month():
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
        response = client.get(f'/api/v1/incomes/?month={previous_month}', headers={
            "Authorization": f"Bearer {token}"
        })
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) == 1


def test_get_total_incomes_for_previous_month():
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
        response = client.get(f'/api/v1/incomes/total/?month={previous_month}', headers={
            "Authorization": f"Bearer {token}"
        })
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['totalIncomes'] == 100


def test_get_all_incomes_for_next_month():
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
        response = client.get(f'/api/v1/incomes/?month={next_month}', headers={
            "Authorization": f"Bearer {token}"
        })
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) == 0


def test_get_total_incomes_for_next_month():
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
        response = client.get(f'/api/v1/incomes/total/?month={next_month}', headers={
            "Authorization": f"Bearer {token}"
        })
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['totalIncomes'] == 0


def test_delete_income():
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
        response = client.delete(f'/api/v1/incomes/1/', headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 204


def test_delete_doesnt_exist_income():
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
        response = client.delete(f'/api/v1/incomes/10/', headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 404

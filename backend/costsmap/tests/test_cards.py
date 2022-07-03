from .main import client, clean_testing


def test_create_card():
    clean_testing()
    with client:
        response = client.post('/api/v1/auth/registration/', json={
            "email": "someone@gmail.com",
            "password1": "Password123",
            "password2": "Password123",
            "currency": "$",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.post('/api/v1/cards/', headers={
            "Authorization": f"Bearer {token}",
        }, json={
            "title": "Some card",
            "currency": "$",
            "color": "#333333",
        })
        assert response.status_code == 201
        assert response.json() == {
            "title": "Some card",
            "currency": "$",
            "color": "#333333",
            "amount": 0,
            "id": 1
        }


def test_create_card_with_already_exists_title():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.post('/api/v1/cards/', headers={
            "Authorization": f"Bearer {token}",
        }, json={
            "title": "Some card",
            "currency": "$",
            "color": "#333333",
        })
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Card with this title already exists"
        }


def test_create_card_with_incorrect_fields():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.post('/api/v1/cards/', headers={
            "Authorization": f"Bearer {token}",
        }, json={
            "title": "Some card",
            "currency": "j",
            "color": "#333333",
        })
        assert response.status_code == 422


def test_get_all_cards():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.get('/api/v1/cards/', headers={
            "Authorization": f"Bearer {token}",
        })
        assert response.status_code == 200
        assert response.json() == [{
            "title": "Some card",
            "currency": "$",
            "color": "#333333",
            "id": 1,
            "amount": 0
        }]


def test_get_concrete_card():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.get('/api/v1/cards/1/', headers={
            "Authorization": f"Bearer {token}",
        })
        assert response.status_code == 200
        assert response.json() == {
            "title": "Some card",
            "currency": "$",
            "color": "#333333",
            "id": 1,
            "amount": 0
        }


def test_get_concrete_card_with_doesnt_exist_id():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.get('/api/v1/cards/4/', headers={
            "Authorization": f"Bearer {token}",
        })
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Card with this id doesn't exist"
        }


def test_update_concrete_card():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.put('/api/v1/cards/1/', headers={
            "Authorization": f"Bearer {token}",
        }, json={
            "title": "New card title",
            "currency": "$",
            "color": "#333333",
        })
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "title": "New card title",
            "currency": "$",
            "color": "#333333",
            "amount": 0,
        }


def test_update_concrete_card_with_doesnt_exist_id():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.put('/api/v1/cards/4/', headers={
            "Authorization": f"Bearer {token}",
        }, json={
            "title": "New card title",
            "currency": "$",
            "color": "#333333",
        })
        assert response.status_code == 404


def test_update_concrete_card_with_already_exist_title():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.post('/api/v1/cards/', headers={
            "Authorization": f"Bearer {token}",
        }, json={
            "title": "Some card1",
            "currency": "$",
            "color": "#333333",
        })
        assert response.status_code == 201
        response = client.put('/api/v1/cards/1/', headers={
            "Authorization": f"Bearer {token}",
        }, json={
            "title": "Some card1",
            "currency": "$",
            "color": "#333333",
        })
        assert response.status_code == 400
        assert response.json() == {
            'detail': 'Card with this title already exists'
        }


def test_delete_concrete_card():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.post('/api/v1/cards/', headers={
            "Authorization": f"Bearer {token}",
        }, json={
            "title": "Some card2",
            "currency": "$",
            "color": "#333333",
        })
        assert response.status_code == 201
        response = client.delete('/api/v1/cards/1/', headers={
            "Authorization": f"Bearer {token}",
        })
        assert response.status_code == 204


def test_delete_concrete_card_with_doesnt_exist_id():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = data['token']
        response = client.delete('/api/v1/cards/96/', headers={
            "Authorization": f"Bearer {token}",
        })
        assert response.status_code == 404

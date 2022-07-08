from .main import client, clean_testing


def test_registration():
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
        assert 'exptime' in data


def test_registration_without_currency():
    with client:
        response = client.post('/api/v1/auth/registration/', json={
            "email": "someone2@gmail.com",
            "password1": "Password123",
            "password2": "Password123",
        })
        assert response.status_code == 422


def test_registration_with_incorrect_currency():
    with client:
        response = client.post('/api/v1/auth/registration/', json={
            "email": "someone2@gmail.com",
            "password1": "Password123",
            "password2": "Password123",
            "currency": "j",
        })
        assert response.status_code == 422


def test_registration_with_different_passwords():
    with client:
        response = client.post('/api/v1/auth/registration/', json={
            "email": "someone2@gmail.com",
            "password1": "Password123",
            "password2": "Password125",
            "currency": "$",
        })
        assert response.status_code == 422


def test_registration_with_not_valid_password():
    with client:
        response = client.post('/api/v1/auth/registration/', json={
            "email": "someone2@gmail.com",
            "password1": "pass",
            "password2": "pass",
            "currency": "$",
        })
        assert response.status_code == 422


def test_registration_with_already_exists_email():
    with client:
        response = client.post('/api/v1/auth/registration/', json={
            "email": "someone@gmail.com",
            "password1": "Password123",
            "password2": "Password123",
            "currency": "$",
        })
        assert response.status_code == 400
        data = response.json()
        assert data['detail'] == 'User with this email already exists'


def test_login():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        assert 'exptime' in data


def test_login_with_incorrect_password():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password125"
        })
        assert response.status_code == 400
        data = response.json()
        assert data['detail'] == 'Incorrect password'


def test_me():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = response.json()['token']
        response = client.get('/api/v1/auth/me/', headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 200
        assert response.json() == {
            "email": "someone@gmail.com",
            "currency": "$",
            "id": 1
        }


def test_me_with_incorrect_token():
    with client:
        response = client.get('/api/v1/auth/me/', headers={
            'Authorization': f'Bearer incorrect_token'
        })
        assert response.status_code == 401


def test_change_me():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = response.json()['token']
        response = client.put('/api/v1/auth/me/', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            "email": "someone@gmail.com",
            "currency": "$",
        })
        assert response.status_code == 200
        print(response.json())
        assert response.json() == {
            "email": "someone@gmail.com",
            "currency": "$",
            "id": 1
        }


def test_change_me_with_email():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone@gmail.com",
            "password": "Password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = response.json()['token']
        response = client.put('/api/v1/auth/me/', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            "email": "someone2@gmail.com",
            "currency": "$",
        })
        assert response.status_code == 200
        print(response.json())
        assert response.json() == {
            "email": "someone2@gmail.com",
            "currency": "$",
            "id": 1
        }


def test_change_password():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone2@gmail.com",
            "password": "Password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = response.json()['token']
        response = client.post('/api/v1/auth/change_password/', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            "oldPassword": "Password123",
            "newPassword": "NewPassword123",
        })
        assert response.status_code == 204


def test_change_password_with_incorrect_old_password():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone2@gmail.com",
            "password": "NewPassword123"
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = response.json()['token']
        response = client.post('/api/v1/auth/change_password/', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            "oldPassword": "Password123",
            "newPassword": "NewPassword123",
        })
        assert response.status_code == 400


def test_change_password_with_incorrect_new_password():
    with client:
        response = client.post('/api/v1/auth/login/', json={
            "email": "someone2@gmail.com",
            "password": "NewPassword123"
        })
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        token = response.json()['token']
        response = client.post('/api/v1/auth/change_password/', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            "oldPassword": "NewPassword123",
            "newPassword": "pass",
        })
        assert response.status_code == 422


def test_get_supported_currencies():
    with client:
        response = client.get('/api/v1/auth/currencies/')
        assert response.status_code == 200
        assert response.json() == {
            "currencies": ["₽", "$", "€", "¥"]
        }

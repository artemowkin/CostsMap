from .main import setup_testing, client, clean_testing


def test_registration():
    clean_testing()
    setup_testing()
    response = client.post('/api/v1/auth/registration/', json={
        "email": "someone@gmail.com",
        "password1": "Password123",
        "password2": "Password123",
        "currency": "$",
        "language": "english",
    })
    assert response.status_code == 200
    data = response.json()
    assert 'token' in data
    assert 'exptime' in data


def test_registration_without_language():
    response = client.post('/api/v1/auth/registration/', json={
        "email": "someone2@gmail.com",
        "password1": "Password123",
        "password2": "Password123",
        "currency": "$"
    })
    assert response.status_code == 422


def test_registration_without_currency():
    response = client.post('/api/v1/auth/registration/', json={
        "email": "someone2@gmail.com",
        "password1": "Password123",
        "password2": "Password123",
        "language": "russian"
    })
    assert response.status_code == 422


def test_registration_with_incorrect_language():
    response = client.post('/api/v1/auth/registration/', json={
        "email": "someone2@gmail.com",
        "password1": "Password123",
        "password2": "Password123",
        "currency": "$",
        "language": "incorrect"
    })
    assert response.status_code == 422


def test_registration_with_incorrect_currency():
    response = client.post('/api/v1/auth/registration/', json={
        "email": "someone2@gmail.com",
        "password1": "Password123",
        "password2": "Password123",
        "currency": "j",
        "language": "russian"
    })
    assert response.status_code == 422


def test_registration_with_different_passwords():
    response = client.post('/api/v1/auth/registration/', json={
        "email": "someone2@gmail.com",
        "password1": "Password123",
        "password2": "Password125",
        "currency": "$",
        "language": "russian"
    })
    assert response.status_code == 422


def test_registration_with_not_valid_password():
    response = client.post('/api/v1/auth/registration/', json={
        "email": "someone2@gmail.com",
        "password1": "pass",
        "password2": "pass",
        "currency": "$",
        "language": "russian"
    })
    assert response.status_code == 422


def test_registration_with_already_exists_email():
    response = client.post('/api/v1/auth/registration/', json={
        "email": "someone@gmail.com",
        "password1": "Password123",
        "password2": "Password123",
        "currency": "$",
        "language": "english",
    })
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == 'User with this email already exists'


def test_login():
    response = client.post('/api/v1/auth/login/', json={
        "email": "someone@gmail.com",
        "password": "Password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert 'token' in data
    assert 'exptime' in data


def test_login_with_incorrect_password():
    response = client.post('/api/v1/auth/login/', json={
        "email": "someone@gmail.com",
        "password": "Password125"
    })
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == 'Incorrect password'


def test_me():
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
        "language": "english",
        "id": 1
    }


def test_me_with_incorrect_token():
    response = client.get('/api/v1/auth/me/', headers={
        'Authorization': f'Bearer incorrect_token'
    })
    assert response.status_code == 401


def test_change_me():
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
        "language": "russian"
    })
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "email": "someone@gmail.com",
        "currency": "$",
        "language": "russian",
        "id": 1
    }


def test_change_me_with_email():
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
        "language": "english"
    })
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "email": "someone2@gmail.com",
        "currency": "$",
        "language": "english",
        "id": 1
    }


def test_change_me_with_incorrect_language():
    response = client.post('/api/v1/auth/login/', json={
        "email": "someone2@gmail.com",
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
        "language": "incorrect"
    })
    assert response.status_code == 422


def test_change_password():
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
        "old_password": "Password123",
        "new_password": "NewPassword123",
    })
    assert response.status_code == 204


def test_change_password_with_incorrect_old_password():
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
        "old_password": "Password123",
        "new_password": "NewPassword123",
    })
    assert response.status_code == 400


def test_change_password_with_incorrect_new_password():
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
        "old_password": "NewPassword123",
        "new_password": "pass",
    })
    assert response.status_code == 422


def test_get_supported_languages():
    response = client.get('/api/v1/auth/languages/')
    assert response.status_code == 200
    assert response.json() == {
        "languages": ["russian", "english"]
    }


def test_get_supported_currencies():
    response = client.get('/api/v1/auth/currencies/')
    assert response.status_code == 200
    assert response.json() == {
        "currencies": ["₽", "$", "€", "¥"]
    }

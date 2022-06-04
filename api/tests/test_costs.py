from .main import setup_testing, client, clean_testing


def test_get_all_costs_with_empty_db():
    clean_testing()
    setup_testing()
    response = client.post('/api/v1/auth/registration/', json={
        "email": "someone@gmail.com",
        "password1": "Password123",
        "password2": "Password123",
        "currency": "$",
        "language": "english",
    })
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert 'token' in data
    token = data['token']
    response = client.get('/api/v1/costs/', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json() == []

import pytest
from httpx import AsyncClient

import settings


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_register_success():
    user_json = {
        'first_name': 'test',
        'middle_name': 'burh',
        'last_name': 'grfdghrfgh',
        'delivery_address': 'Syhiv',
        'phone_number': 380995762844,
        'email': 'test2@gmail.com',
        'password': 'testpass',
        'role': 'test'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.post('/register', json=user_json)
        assert res.status_code == 201

        token = await client.post('/login', json={
            'email': user_json['email'],
            'password': user_json['password']
        })
        token = token.json()
        await client.delete('/delete', headers={
            'Authorization': f'Bearer {token}'
        })


@pytest.mark.anyio
async def test_register_email_exists():
    user_json = {
        'first_name': 'test',
        'middle_name': 'burh',
        'last_name': 'grfdghrfgh',
        'delivery_address': 'Syhiv',
        'phone_number': 380995762844,
        'email': 'test@gmail.com',
        'password': 'testpass',
        'role': 'test'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.post('/register', json=user_json)
        assert res.status_code == 400


@pytest.mark.anyio
async def test_register_wrong_phone_number():
    user_json = {
        'first_name': 'test',
        'middle_name': 'burh',
        'last_name': 'grfdghrfgh',
        'delivery_address': 'Syhiv',
        'phone_number': 3809945762844,
        'email': 'test2@gmail.com',
        'password': 'megapass228',
        'role': 'test'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.post('/register', json=user_json)
        assert res.status_code == 422


@pytest.mark.anyio
async def test_login_success():
    login_data = {
        'email': 'test@gmail.com',
        'password': 'testpass'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.post('/login', json=login_data)
        assert res.status_code == 200
        assert res.json() == (
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1NWE3MGY4MTM3YmFkMThjY2JmODdkZCIsImVtYWlsIjoidGVzdEBnbWFpb'
            'C5jb20iLCJyb2xlIjoidGVzdCJ9.5loRcVbwlLTHyWdbbKg7x-AOXjTOo6JYEVPpU_HLbPI')


@pytest.mark.anyio
async def test_login_wrong_email():
    login_data = {
        'email': 'test5@gmail.com',
        'password': 'testpass'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.post('/login', json=login_data)
        assert res.status_code == 400


@pytest.mark.anyio
async def test_login_wrong_password():
    login_data = {
        'email': 'test@gmail.com',
        'password': 'test5pass'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.post('/login', json=login_data)
        assert res.status_code == 400


@pytest.mark.anyio
async def test_login_attempts():
    login_data = {
        'email': 'test@gmail.com',
        'password': 'test5pass'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        for _ in range(2):
            await client.post('/login', json=login_data)
        res = await client.post('/login', json=login_data)
        assert res.status_code == 400
        assert res.json() == {'detail': 'Reached login attempts limit'}

        reset_res = await client.post('/reset-user-login-atts', headers={
            'X-Key': settings.SECRET_TOKEN
        }, json={
            'email': 'test@gmail.com'
        })
        assert reset_res.status_code == 200


@pytest.mark.anyio
async def test_user_get():
    user_json = {
        'first_name': 'test',
        'middle_name': 'test',
        'last_name': 'test',
        'delivery_address': 'test',
        'phone_number': 380994652744,
        'email': 'test@gmail.com',
        '_id': '655a70f8137bad18ccbf87dd'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        await client.post('/register', json=user_json)

        token = await client.post('/login', json={
            'email': user_json['email'],
            'password': 'testpass'
        })
        token = token.json()

        res = await client.get('/get-info', headers={
            'Authorization': f'Bearer {token}'
        })
        assert res.status_code == 200
        assert res.json() == user_json


@pytest.mark.anyio
async def test_user_update():
    user_json = {
        'first_name': 'update',
        'middle_name': 'burh',
        'last_name': 'grfdghrfgh',
        'delivery_address': 'Syhiv',
        'phone_number': 380994576284,
        'email': 'test2update@gmail.com',
        'password': 'megapass228',
        'role': 'test'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        await client.post('/register', json=user_json)

        token = await client.post('/login', json={
            'email': user_json['email'],
            'password': user_json['password']
        })
        token = token.json()

        user_json_update = {
            'first_name': 'update2',
            'middle_name': 'bruh',
            'last_name': 'grfdghrfgh',
            'delivery_address': 'Syhiv',
            'phone_number': 380994576284,
        }

        updated_user = await client.put('/update-info', headers={
            'Authorization': f'Bearer {token}'
        }, json=user_json_update)

        user_json_update['email'] = user_json['email']

        assert updated_user.status_code == 200
        assert updated_user.json() == user_json_update

        await client.delete('/delete', headers={
            'Authorization': f'Bearer {token}'
        })


@pytest.mark.anyio
async def test_user_delete():
    user_json = {
        'first_name': 'delete',
        'middle_name': 'burh',
        'last_name': 'grfdghrfgh',
        'delivery_address': 'Syhiv',
        'phone_number': 380994576284,
        'email': 'test2delete@gmail.com',
        'password': 'megapass228',
        'role': 'test'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        await client.post('/register', json=user_json)
        token = await client.post('/login', json={
            'email': user_json['email'],
            'password': user_json['password']
        })
        token = token.json()
        res = await client.delete('/delete', headers={
            'Authorization': f'Bearer {token}'
        })
        assert res.status_code == 204

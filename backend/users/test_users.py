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
        'date_of_birth': '2002-12-12',
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
            'Authorization': f'Bearer {token["access_token"]}'
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
        'date_of_birth': '2002-12-12',
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
        'date_of_birth': '2002-12-12',
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
async def test_user_update():
    user_json = {
        'first_name': 'update',
        'middle_name': 'burh',
        'last_name': 'grfdghrfgh',
        'delivery_address': 'Syhiv',
        'phone_number': 380994576284,
        'email': 'test2update@gmail.com',
        'password': 'megapass228',
        'date_of_birth': '2001-08-05',
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
            'date_of_birth': '2001-09-14'
        }

        updated_user = await client.put('/update-info', headers={
            'Authorization': f'Bearer {token["access_token"]}'
        }, json=user_json_update)

        user_json_update['email'] = user_json['email']

        assert updated_user.status_code == 200
        assert updated_user.json() == user_json_update

        await client.delete('/delete', headers={
            'Authorization': f'Bearer {token["access_token"]}'
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
        'date_of_birth': '2001-08-05',
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
            'Authorization': f'Bearer {token["access_token"]}'
        })
        assert res.status_code == 204


ADMIN_TEST_USER_ID = ''


@pytest.mark.anyio
async def test_admin_user_delete_not_admin():
    global ADMIN_TEST_USER_ID
    user_json = {
        'first_name': 'delete',
        'middle_name': 'burh',
        'last_name': 'grfdghrfgh',
        'delivery_address': 'Syhiv',
        'phone_number': 380994576284,
        'email': 'test2delete@gmail.com',
        'date_of_birth': '2001-08-05',
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

        user = await client.get('/get-info', headers={
            'Authorization': f'Bearer {token["access_token"]}'
        })
        user_data = user.json()
        ADMIN_TEST_USER_ID = user_data['_id']

        del_res = await client.delete(f'/delete/{ADMIN_TEST_USER_ID}', headers={
            'Authorization': f'Bearer {token["access_token"]}'
        })
        assert del_res.status_code == 401


@pytest.mark.anyio
async def test_admin_user_get_success():
    user_json = {
        '_id': ADMIN_TEST_USER_ID,
        'first_name': 'delete',
        'middle_name': 'burh',
        'last_name': 'grfdghrfgh',
        'delivery_address': 'Syhiv',
        'phone_number': 380994576284,
        'email': 'test2delete@gmail.com',
        'date_of_birth': '2001-08-05',
        'role': 'test'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.get(f'/get-info/{ADMIN_TEST_USER_ID}', headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })
        assert res.status_code == 200
        res = res.json()
        assert res == user_json


@pytest.mark.anyio
async def test_advanced_user_get_success():
    user_json = {
        'first_name': 'delete',
        'email': 'test2delete@gmail.com'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.get(f'/get-info/{ADMIN_TEST_USER_ID}', headers={
            'Authorization': f'Bearer {settings.ADVANCED_TOKEN}'
        })
        assert res.status_code == 200
        res = res.json()
        assert res == user_json


@pytest.mark.anyio
async def test_advanced_user_get_not_admin_or_advanced():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.get(f'/get-info/{ADMIN_TEST_USER_ID}', headers={
            'Authorization': f'Bearer {settings.USER_TOKEN}'
        })
        assert res.status_code == 401


@pytest.mark.anyio
async def test_admin_user_delete_success():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        del_res = await client.delete(f'/delete/{ADMIN_TEST_USER_ID}', headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })
        assert del_res.status_code == 204


@pytest.mark.anyio
async def test_admin_send_emails_success():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.post(f'/send-emails/12', headers={
            'Authorization': f'Bearer {settings.ADVANCED_TOKEN}'
        })
        assert res.status_code == 200

        res = res.json()
        assert res == [
            {
                "to": "andriyko@gmail.com",
                "message": "Hello Andriyko, you have 10% discount for this month in example.shop.com\""
            },
            {
                "to": "test@gmail.com",
                "message": "Hello test, you have 10% discount for this month in example.shop.com\""
            }
        ]


@pytest.mark.anyio
async def test_admin_send_emails_empty():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.post(f'/send-emails/02', headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })
        assert res.status_code == 200
        res = res.json()
        assert res == []


@pytest.mark.anyio
async def test_admin_send_emails_not_admin_or_advanced():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.post(f'/send-emails/12', headers={
            'Authorization': f'Bearer {settings.USER_TOKEN}'
        })
        assert res.status_code == 401


@pytest.mark.anyio
async def test_admin_send_emails_wrong_month():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/users') as client:
        res = await client.post(f'/send-emails/15', headers={
            'Authorization': f'Bearer {settings.ADVANCED_TOKEN}'
        })
        assert res.status_code == 400
        res = res.json()
        assert res == {'detail': "Month can't be less than 1 and more than 12"}

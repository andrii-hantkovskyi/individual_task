import pytest
from httpx import AsyncClient

import settings

TEST_PRODUCT_ID = '655bb6f37b5ff4dbc7253cd5'


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_get_product_by_id():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        res = await client.get(f'/{TEST_PRODUCT_ID}')
        assert res.status_code == 200
        assert res.json() == {
            '_id': TEST_PRODUCT_ID,
            'type': 'test',
            'name': 'test'
        }


@pytest.mark.anyio
async def test_product_create_success():
    product_json = {
        'type': 'test',
        'name': 'test5'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        res = await client.post('/', json=product_json, headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })
        assert res.status_code == 201
        res = res.json()

        await client.delete(f'/{res["_id"]}', headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })


@pytest.mark.anyio
async def test_product_create_unauthorized():
    product_json = {
        'type': 'test',
        'name': 'test5'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        res = await client.post('/', json=product_json)
        assert res.status_code == 401


@pytest.mark.anyio
async def test_product_create_not_admin():
    product_json = {
        'type': 'test',
        'name': 'test5'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        token = await client.request(method='POST', url='http://127.0.0.1:8000/api/users/login', json={
            'email': 'test@gmail.com',
            'password': 'testpass'
        })

        token = token.json()

        res = await client.post('/', json=product_json, headers={
            'Authorization': f'Bearer {token["access"]}'
        })
        assert res.status_code == 401


@pytest.mark.anyio
async def test_product_create_wrong_type():
    product_json = {
        'type': 'wrong',
        'name': 'test5'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        res = await client.post('/', json=product_json, headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })
        assert res.status_code == 422


@pytest.mark.anyio
async def test_product_create_existing_name():
    product_json = {
        'type': 'test',
        'name': 'test'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        res = await client.post('/', json=product_json, headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })
        assert res.status_code == 400
        assert res.json() == {'detail': 'Product with such name already exists'}


@pytest.mark.anyio
async def test_product_update_success():
    update_json = {
        'type': 'test',
        'name': 'test_updated'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        res = await client.put(f'/{TEST_PRODUCT_ID}', json=update_json, headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })

        assert res.status_code == 200
        assert res.json() == {
            '_id': TEST_PRODUCT_ID,
            **update_json
        }

        await client.put(f'/{TEST_PRODUCT_ID}', json={
            'type': 'test',
            'name': 'test'
        }, headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })


@pytest.mark.anyio
async def test_product_update_unauthorized():
    product_json = {
        'type': 'test',
        'name': 'test5'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        res = await client.put(f'/{TEST_PRODUCT_ID}', json=product_json)
        assert res.status_code == 401


@pytest.mark.anyio
async def test_product_update_not_admin():
    product_json = {
        'type': 'test',
        'name': 'test5'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        token = await client.request(method='POST', url='http://127.0.0.1:8000/api/users/login', json={
            'email': 'test@gmail.com',
            'password': 'testpass'
        })

        token = token.json()

        res = await client.put(f'/{TEST_PRODUCT_ID}', json=product_json, headers={
            'Authorization': f'Bearer {token["access"]}'
        })
        assert res.status_code == 401


@pytest.mark.anyio
async def test_product_update_wrong_type():
    update_json = {
        'type': 'wrong',
        'name': 'test_updated'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        res = await client.put(f'/{TEST_PRODUCT_ID}', json=update_json, headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })
        assert res.status_code == 422


@pytest.mark.anyio
async def test_product_update_name_exists():
    update_json = {
        'type': 'test',
        'name': 'test'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        res = await client.put(f'/{TEST_PRODUCT_ID}', json=update_json, headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })

        assert res.status_code == 400
        assert res.json() == {'detail': 'Product with such name already exists'}


@pytest.mark.anyio
async def test_product_delete_success():
    product_json = {
        'type': 'test',
        'name': 'test_for_delete'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        res = await client.post('/', json=product_json, headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })

        res = res.json()

        del_res = await client.delete(f'/{res["_id"]}', headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })

        assert del_res.status_code == 204


@pytest.mark.anyio
async def test_product_delete_unauthorized():
    product_json = {
        'type': 'test',
        'name': 'test_for_delete'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        res = await client.post('/', json=product_json, headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })
        res = res.json()

        del_res = await client.delete(f'/{res["_id"]}')

        assert del_res.status_code == 401

        await client.delete(f'/{res["_id"]}', headers={'Authorization': f'Bearer {settings.ADMIN_TOKEN}'})


@pytest.mark.anyio
async def test_product_delete_not_admin():
    product_json = {
        'type': 'test',
        'name': 'test_for_delete'
    }

    async with AsyncClient(base_url='http://127.0.0.1:8000/api/products') as client:
        res = await client.post('/', json=product_json, headers={
            'Authorization': f'Bearer {settings.ADMIN_TOKEN}'
        })
        res = res.json()

        del_res = await client.delete(f'/{res["_id"]}', headers={
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1NWE3MGY4MTM3YmFkMThjY2JmODdkZCIsI'
                             'mVtYWlsIjoidGVzdEBnbWFpbC5jb20iLCJyb2xlIjoidGVzdCJ9.5loRcVbwlLTHyWdbbKg7x-AOXjTOo6JYEVPpU'
                             '_HLbPI'
        })

        assert del_res.status_code == 401

        await client.delete(f'/{res["_id"]}', headers={'Authorization': f'Bearer {settings.ADMIN_TOKEN}'})

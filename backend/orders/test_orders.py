import pytest
from httpx import AsyncClient

import settings

TEST_ORDER_ID = '655cd2232a457d0178c772d4'
TEST_USER_TOKEN = (
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1NWNjYjM4YTNjMmIwMTc1N2UxOTI0MCIsImVtYWlsIjoidGVzdE'
    'BnbWFpbC5jb20iLCJyb2xlIjoidGVzdCJ9.eXQy3CUHnPW6Dh1_pKkVad8f5RojUygcDOuGQI2D5xw'
)
TEST_PRODUCT_ID = '655bb6f37b5ff4dbc7253cd5'
TEST_PRODUCT2_ID = '655cd4d73aad6333ef941437'

TEST_ORDER_PROCESS_ID = ''


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_order_get_by_id_success():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/orders') as client:
        res = await client.get(f'/{TEST_ORDER_ID}', headers={'Authorization': f'Bearer {TEST_USER_TOKEN}'})
        assert res.status_code == 200
        assert res.json() == {
            '_id': TEST_ORDER_ID,
            'product_id': TEST_PRODUCT_ID,
            'qty': 4
        }


@pytest.mark.anyio
async def test_order_get_by_id_unauthorized():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/orders') as client:
        res = await client.get(f'/{TEST_ORDER_ID}')
        assert res.status_code == 401


@pytest.mark.anyio
async def test_order_create_success():
    global TEST_ORDER_PROCESS_ID
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/orders') as client:
        order_json = {
            'product_id': TEST_PRODUCT2_ID,
            'qty': 1
        }

        res = await client.post('/', json=order_json, headers={'Authorization': f'Bearer {TEST_USER_TOKEN}'})
        assert res.status_code == 201

        res = res.json()
        TEST_ORDER_PROCESS_ID = res['_id']


@pytest.mark.anyio
async def test_order_create_unauthorized():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/orders') as client:
        order_json = {
            'product_id': TEST_PRODUCT2_ID,
            'qty': 1
        }

        res = await client.post('/', json=order_json, )
        assert res.status_code == 401


@pytest.mark.anyio
async def test_order_create_wrong_qty():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/orders') as client:
        order_json = {
            'product_id': TEST_PRODUCT2_ID,
            'qty': 0
        }

        res = await client.post('/', json=order_json, headers={'Authorization': f'Bearer {TEST_USER_TOKEN}'})
        assert res.status_code == 422


@pytest.mark.anyio
async def test_order_create_wrong_product():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/orders') as client:
        order_json = {
            'product_id': '59823479568hr7',
            'qty': 0
        }

        res = await client.post('/', json=order_json, headers={'Authorization': f'Bearer {TEST_USER_TOKEN}'})
        assert res.status_code == 422


@pytest.mark.anyio
async def test_order_create_exists():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/orders') as client:
        order_json = {
            'product_id': TEST_PRODUCT2_ID,
            'qty': 1
        }

        res = await client.post('/', json=order_json, headers={'Authorization': f'Bearer {TEST_USER_TOKEN}'})
        assert res.status_code == 400
        assert res.json() == {'detail': 'Order already exists'}


@pytest.mark.anyio
async def test_order_delete_unauthorized():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/orders') as client:
        res = await client.delete(f'/{TEST_ORDER_PROCESS_ID}')
        assert res.status_code == 401


@pytest.mark.anyio
async def test_order_delete_wrong_user():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/orders') as client:
        res = await client.delete(f'/{TEST_ORDER_PROCESS_ID}',
                                  headers={'Authorization': f'Bearer {settings.ADMIN_TOKEN}'})
        assert res.status_code == 404


@pytest.mark.anyio
async def test_order_delete_wrong_product():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/orders') as client:
        res = await client.delete(f'/{TEST_PRODUCT_ID}', headers={'Authorization': f'Bearer {TEST_USER_TOKEN}'})
        assert res.status_code == 404


@pytest.mark.anyio
async def test_order_delete_success():
    async with AsyncClient(base_url='http://127.0.0.1:8000/api/orders') as client:
        res = await client.delete(f'/{TEST_ORDER_PROCESS_ID}', headers={'Authorization': f'Bearer {TEST_USER_TOKEN}'})
        assert res.status_code == 204

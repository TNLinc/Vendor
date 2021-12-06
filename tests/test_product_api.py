import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_get_all_products(client, fill_product_data, jsonify):
    expected = {
        "items": [
            {
                "name": "Amazing cream",
                "type": 1,
                "url": "https://www.letu.ru/Amazing%20cream",
                "id": "c40d6f3d-f617-4edb-adc7-ab67c0d643f7",
                "color": {
                    "id": "85e6df48-a150-4be1-ba0b-9f6cef0f50d1",
                    "name": "Green",
                    "color": "#B8E981",
                },
            },
            {
                "name": "Wonderful cream",
                "type": 1,
                "url": "https://www.dior.com/Wonderful%20cream",
                "id": "694afe5d-5fdc-42c8-8a91-40fc2142a436",
                "color": {
                    "id": "becdc231-7c75-4d39-837c-0aa27462d10d",
                    "name": "Red",
                    "color": "#D90000",
                },
            },
        ],
        "total": 2,
        "page": 1,
        "size": 50,
    }
    response: Response = await client.get("/api/vendor/v1/products/default/")
    assert response.status_code == 200
    assert response.read() == jsonify(expected)


@pytest.mark.asyncio
async def test_get_all_products_sort_by_color(client, fill_product_data, jsonify):
    expected = {
        "items": [
            {
                "name": "Wonderful cream",
                "type": 1,
                "url": "https://www.dior.com/Wonderful%20cream",
                "id": "694afe5d-5fdc-42c8-8a91-40fc2142a436",
                "color": {
                    "id": "becdc231-7c75-4d39-837c-0aa27462d10d",
                    "name": "Red",
                    "color": "#D90000",
                },
            },
            {
                "name": "Amazing cream",
                "type": 1,
                "url": "https://www.letu.ru/Amazing%20cream",
                "id": "c40d6f3d-f617-4edb-adc7-ab67c0d643f7",
                "color": {
                    "id": "85e6df48-a150-4be1-ba0b-9f6cef0f50d1",
                    "name": "Green",
                    "color": "#B8E981",
                },
            },
        ],
        "total": 2,
        "page": 1,
        "size": 50,
    }
    response: Response = await client.get(
        "/api/vendor/v1/products/default/?color=%23444444"
    )
    assert response.status_code == 200
    assert response.read() == jsonify(expected)


@pytest.mark.asyncio
async def test_get_product(client, fill_product_data, jsonify):
    expected = {
        "name": "Amazing cream",
        "type": 1,
        "url": "https://www.letu.ru/Amazing%20cream",
        "id": "c40d6f3d-f617-4edb-adc7-ab67c0d643f7",
        "color": {
            "id": "85e6df48-a150-4be1-ba0b-9f6cef0f50d1",
            "name": "Green",
            "color": "#B8E981",
        },
        "vendor": {
            "name": "Letual",
            "url": "https://www.letu.ru",
            "id": "1ea25152-ccb6-4be0-b269-b8952c88f9a9",
        },
    }
    response: Response = await client.get(
        "/api/vendor/v1/products/c40d6f3d-f617-4edb-adc7-ab67c0d643f7"
    )
    assert response.status_code == 200
    assert response.read() == jsonify(expected)

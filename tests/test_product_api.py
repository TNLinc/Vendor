import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_get_all_products(client, fill_product_data, jsonify):
    expected = {
        "items": [
            {
                "name": "Amazing cream",
                "type": 1,
                "color": "#666666",
                "id": "c40d6f3d-f617-4edb-adc7-ab67c0d643f7",
            },
            {
                "name": "Wonderful creamm",
                "type": 1,
                "color": "#444444",
                "id": "694afe5d-5fdc-42c8-8a91-40fc2142a436",
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
                "color": "#444444",
                "id": "694afe5d-5fdc-42c8-8a91-40fc2142a436",
            },
            {
                "name": "Amazing cream",
                "type": 1,
                "color": "#666666",
                "id": "c40d6f3d-f617-4edb-adc7-ab67c0d643f7",
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
        "color": "#666666",
        "id": "c40d6f3d-f617-4edb-adc7-ab67c0d643f7",
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

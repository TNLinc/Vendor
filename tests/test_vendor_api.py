import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_get_all_vendors(client, fill_vendor_data, jsonify):
    expected = [
        {
            "name": "Letual",
            "url": "https://www.letu.ru",
            "id": "1ea25152-ccb6-4be0-b269-b8952c88f9a9",
        },
        {
            "name": "Dior",
            "url": "https://www.dior.com/ru_ru",
            "id": "d8974f35-0ba5-42b8-a483-67c5062b9e3e",
        },
    ]
    response: Response = await client.get("/api/vendor/v1/vendors")
    assert response.status_code == 200
    assert response.read() == jsonify(expected)


@pytest.mark.asyncio
async def test_get_vendor(client, fill_product_data, jsonify):
    expected = {
        "name": "Letual",
        "url": "https://www.letu.ru",
        "id": "1ea25152-ccb6-4be0-b269-b8952c88f9a9",
        "products": [
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
            }
        ],
    }
    response: Response = await client.get(
        "/api/vendor/v1/vendors/1ea25152-ccb6-4be0-b269-b8952c88f9a9"
    )

    assert response.status_code == 200
    assert response.read() == jsonify(expected)

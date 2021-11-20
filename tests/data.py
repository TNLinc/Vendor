from models import ProductType

vendors = [
    {
        "id": "1ea25152-ccb6-4be0-b269-b8952c88f9a9",
        "name": "Letual",
        "url": "https://www.letu.ru",
    },
    {
        "id": "d8974f35-0ba5-42b8-a483-67c5062b9e3e",
        "name": "Dior",
        "url": "https://www.dior.com/ru_ru",
    },
]

products = [
    {
        "id": "c40d6f3d-f617-4edb-adc7-ab67c0d643f7",
        "name": "Amazing cream",
        "type": ProductType.TONAL_CREAM,
        "color": "#666666",
        "vendor_id": vendors[0]["id"],
    },
    {
        "id": "694afe5d-5fdc-42c8-8a91-40fc2142a436",
        "name": "Wonderful cream",
        "type": ProductType.TONAL_CREAM,
        "color": "#444444",
        "vendor_id": vendors[1]["id"],
    },
]

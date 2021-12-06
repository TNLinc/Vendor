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

vendor_colors = [
    {
        "id": "85e6df48-a150-4be1-ba0b-9f6cef0f50d1",
        "name": "Green",
        "color": "#B8E981",
        "vendor_id": "1ea25152-ccb6-4be0-b269-b8952c88f9a9",
    },
    {
        "id": "becdc231-7c75-4d39-837c-0aa27462d10d",
        "name": "Red",
        "color": "#D90000",
        "vendor_id": "d8974f35-0ba5-42b8-a483-67c5062b9e3e",
    },
]

products = [
    {
        "id": "c40d6f3d-f617-4edb-adc7-ab67c0d643f7",
        "name": "Amazing cream",
        "type": ProductType.TONAL_CREAM,
        "color_id": vendor_colors[0]["id"],
        "vendor_id": vendors[0]["id"],
        "url": "https://www.letu.ru/Amazing%20cream",
    },
    {
        "id": "694afe5d-5fdc-42c8-8a91-40fc2142a436",
        "name": "Wonderful cream",
        "type": ProductType.TONAL_CREAM,
        "color_id": vendor_colors[1]["id"],
        "vendor_id": vendors[1]["id"],
        "url": "https://www.dior.com/Wonderful%20cream",
    },
]

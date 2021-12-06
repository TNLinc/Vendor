import json

from httpx import AsyncClient
import pytest
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

import db
from main import app
from models import Product, Vendor, VendorColor
from tests.data import products, vendor_colors, vendors


@pytest.fixture
async def client():
    async with AsyncClient(
        app=app, base_url="http://", headers={"host": "localhost"}
    ) as ac:
        yield ac


@pytest.fixture
def jsonify():
    def inner(json_like: dict):
        return json.dumps(json_like, separators=(",", ":")).encode()

    return inner


@pytest.fixture()
async def session():
    session_generator = db.create_session()
    new_session = await session_generator.__anext__()
    yield new_session
    try:
        await session_generator.__anext__()
    except StopAsyncIteration:
        ...
    finally:
        await db.engine.dispose()


@pytest.fixture
async def fill_vendor_data(session):
    for vendor in vendors:
        session.add(Vendor(**vendor))
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        print("Data already exists! Pass creation.")

    yield

    statement = delete(Vendor)
    await session.execute(statement)
    await session.commit()


@pytest.fixture
async def fill_vendor_color_data(fill_vendor_data, session):
    for color in vendor_colors:
        session.add(VendorColor(**color))
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        print("Data already exists! Pass creation.")

    yield

    statement = delete(VendorColor)
    await session.execute(statement)
    await session.commit()


@pytest.fixture
async def fill_product_data(fill_vendor_color_data, session):
    for product in products:
        session.add(Product(**product))
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        print("Data already exists! Pass creation.")

    yield

    statement = delete(Product)
    await session.execute(statement)
    await session.commit()

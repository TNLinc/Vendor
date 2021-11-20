import json

from httpx import AsyncClient
import pytest
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import db
from main import app
from models import Product, Vendor
from tests import settings
from tests.data import products, vendors


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://") as ac:
        yield ac


@pytest.fixture
async def init_sqlalchemy_engine():
    await db.start_db(settings.TEST_DB_URL)
    yield
    await db.close_db()


@pytest.fixture
def jsonify():
    def inner(json_like: dict):
        return json.dumps(json_like, separators=(",", ":")).encode()

    return inner


@pytest.fixture
async def fill_vendor_data(init_sqlalchemy_engine):
    async with AsyncSession(db.engine) as session:
        for vendor in vendors:
            session.add(Vendor(**vendor))
        try:
            await session.commit()
        except IntegrityError:
            print("Data already exists! Pass creation.")

    yield

    async with AsyncSession(db.engine) as session:
        statement = delete(Vendor)
        await session.execute(statement)
        await session.commit()


@pytest.fixture
async def fill_product_data(fill_vendor_data):
    async with AsyncSession(db.engine) as session:
        for product in products:
            session.add(Product(**product))
        try:
            await session.commit()
        except IntegrityError:
            print("Data already exists! Pass creation.")

    yield

    async with AsyncSession(db.engine) as session:
        statement = delete(Product)
        await session.execute(statement)
        await session.commit()

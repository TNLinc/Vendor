import uuid
from typing import Any, Optional

from fastapi import Depends, HTTPException
from fastapi.params import Query
from fastapi_pagination import LimitOffsetPage, Page, paginate
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic.color import Color
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from db import create_session
from models import Product, ProductRead, ProductWithVendor

router = InferringRouter()


@cbv(router)
class ProductAPI:
    session: AsyncSession = Depends(create_session)

    @router.get("/products/{item_id}", response_model=ProductWithVendor)
    async def get_product(self, item_id: uuid.UUID):
        product = await self.session.get(
            Product, item_id, options=[joinedload(Product.vendor)]
        )
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @router.get(
        "/products/default/",
        response_model=Page[ProductRead],
        summary="Get products with pagination",
    )
    @router.get(
        "/products/limit-offset/",
        response_model=LimitOffsetPage[ProductRead],
        summary="Get products with limit and offset",
    )
    async def get_all_products(
            self, color: Optional[Color] = Query(default=None, description="Sorted color")
    ) -> Any:
        products = await self.session.execute(select(Product))
        products = products.scalars().all()
        if not color:
            return paginate(products)
        return paginate(sorted(products, key=lambda x: x.get_distance(color)))

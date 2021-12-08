import logging
from typing import List
import uuid

from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from db import create_session
from models import Vendor, VendorRead, VendorWithProducts

router = InferringRouter()
log = logging.getLogger("fastapi.request")


@cbv(router)
class VendorAPI:
    session: AsyncSession = Depends(create_session)

    @router.get("/vendors/{item_id}", response_model=VendorWithProducts)
    async def get_vendor(self, item_id: uuid.UUID):
        log.debug("Start processing get_vendor request with id: %s", item_id)
        vendor = await self.session.get(
            Vendor,
            item_id,
            options=[joinedload(Vendor.products), joinedload(Vendor.colors)],
        )

        if not vendor:
            log.debug("Vendor with id: %s not found", item_id)
            raise HTTPException(status_code=404, detail="Vendor not found")

        log.debug("Found vendor with id: %s name: %s", item_id, vendor.name)
        return vendor

    @router.get("/vendors")
    async def get_all_vendors(self) -> List[VendorRead]:
        log.debug("Start processing get_all_vendors")
        stmt = select(Vendor)
        result = await self.session.execute(stmt)
        vendors = result.scalars().all()

        log.debug("Loaded %s vendors", len(vendors))
        return vendors

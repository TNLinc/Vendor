import uuid
from typing import List

from fastapi import Depends
from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from db import create_session
from db import SessionBuilder
from models import Vendor
from models import VendorRead
from models import VendorWithProducts

router = InferringRouter()


@cbv(router)
class VendorAPI:
    session: AsyncSession = Depends(create_session)

    @router.get("/vendors/{item_id}", response_model=VendorWithProducts)
    async def get_vendor(self, item_id: uuid.UUID):
        vendor = await self.session.get(
            Vendor, item_id, options=[joinedload(Vendor.products)]
        )
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")
        return vendor

    @router.get("/vendors")
    async def get_all_vendors(self) -> List[VendorRead]:
        stmt = select(Vendor)
        result = await self.session.execute(stmt)
        return result.scalars().all()

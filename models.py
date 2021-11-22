import enum
import uuid
from typing import List
from typing import Optional

import numpy as np
import sqlalchemy as sa
from PIL import ImageColor
from pydantic import validator
from pydantic.color import Color
from sqlalchemy import Enum
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

from core.config import settings


class VendorBase(SQLModel):
    name: str
    url: str


class Vendor(VendorBase, table=True):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4(), primary_key=True)
    products: List["Product"] = Relationship(back_populates="vendor")

    __table_args__ = {"schema": settings.DB_SCHEMA}

    class Config:
        schema_extra = {
            "example": {
                "id": "028e5753-1992-4f3a-8691-65ba82442c19",
                "name": "Laurel",
                "url": "https://slugify.online",
            }
        }


class VendorRead(VendorBase):
    id: Optional[uuid.UUID]


class ProductType(enum.Enum):
    TONAL_CREAM = 1


class ProductBase(SQLModel):
    name: str
    type: ProductType = Field(sa_column=sa.Column(Enum(ProductType)), nullable=False)
    color: str = Field(nullable=False)

    @validator("color")
    def validate_color(cls, v):
        Color(v)
        return v


class Product(ProductBase, table=True):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4(), primary_key=True)
    vendor_id: uuid.UUID = Field(foreign_key="vendor.vendor.id")
    vendor: Vendor = Relationship(back_populates="products")

    __table_args__ = {"schema": settings.DB_SCHEMA}

    def get_distance(self, target_color: Color):
        target_color = np.array(target_color.as_rgb_tuple())
        product_color = np.array(ImageColor.getrgb(self.color))
        rm = 0.5 * (target_color[0] + product_color[0])
        return sum((2 + rm, 4, 3 - rm) * (target_color[:3] - product_color) ** 2) ** 0.5

    class Config:
        schema_extra = {
            "example": {
                "id": "028e5753-1992-4f3a-8691-65ba82442c19",
                "name": "Cream nature",
                "type": "TONAL_CREAM",
                "color": "#FFA1F8",
                "vendor_id": Vendor.Config.schema_extra,
            }
        }


class ProductRead(ProductBase):
    id: Optional[uuid.UUID]


class VendorWithProducts(VendorRead):
    products: List[ProductRead]


class ProductWithVendor(ProductRead):
    vendor: VendorRead

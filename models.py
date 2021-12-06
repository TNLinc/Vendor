import enum
from math import sqrt
from typing import List, Optional
import uuid

from PIL import ImageColor
import numpy as np
from pydantic import validator
from pydantic.color import Color
import sqlalchemy as sa
from sqlalchemy import Enum
from sqlmodel import Field, Relationship, SQLModel

from core.config import settings


class VendorBase(SQLModel):
    name: str
    url: str


class Vendor(VendorBase, table=True):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4(), primary_key=True)
    products: List["Product"] = Relationship(back_populates="vendor")
    colors: List["VendorColor"] = Relationship(back_populates="vendor")

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


class VendorColorBase(SQLModel):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4(), primary_key=True)
    name: str
    color: str = Field(nullable=False)


class VendorColor(VendorColorBase, table=True):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4(), primary_key=True)
    name: str
    color: str = Field(nullable=False)
    vendor_id: uuid.UUID = Field(foreign_key="vendor.vendor.id")
    vendor: Vendor = Relationship(back_populates="colors")
    products: List["Product"] = Relationship(back_populates="color")

    __tablename__ = "vendor_color"
    __table_args__ = {"schema": settings.DB_SCHEMA}

    @validator("color")
    def validate_color(cls, v):
        Color(v)
        return v


class ProductType(enum.Enum):
    TONAL_CREAM = 1


class ProductBase(SQLModel):
    name: str
    type: ProductType = Field(sa_column=sa.Column(Enum(ProductType)), nullable=False)
    url: str


class Product(ProductBase, table=True):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4(), primary_key=True)
    vendor_id: uuid.UUID = Field(foreign_key="vendor.vendor.id")
    vendor: Vendor = Relationship(back_populates="products")
    color_id: uuid.UUID = Field(foreign_key="vendor.vendor_color.id")
    color: VendorColor = Relationship(back_populates="products")

    __table_args__ = {"schema": settings.DB_SCHEMA}

    def get_distance(self, target_color: Color):
        target_color = np.array(target_color.as_rgb_tuple())
        product_color = np.array(ImageColor.getrgb(self.color.color))
        rm = 0.5 * (target_color[0] + product_color[0])
        return sqrt(
            sum(
                (2 + rm / 256, 4, 2 + (255 - rm) / 256)
                * (target_color[:3] - product_color) ** 2
            )
        )

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
    url: str
    color: VendorColorBase


class VendorWithProducts(VendorRead):
    products: List[ProductRead]


class ProductWithVendor(ProductRead):
    vendor: VendorRead

import logging

import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi_health import health
from fastapi_pagination import add_pagination
from starlette.middleware.trustedhost import TrustedHostMiddleware

import db
from api.v1 import product
from api.v1 import vendor
from core import loger
from core import settings
from core.settings import VENDOR_ALLOWED_HOSTS

description = """
Vendor API helps you do awesome stuff. 🚀

## Vendor

You will be able to:

* **Read vendor by id**
* **Read all vendors**

## Products

You will be able to:

* **Read product by id**
* **Read all products**
* **Get product by color**

"""

tags_metadata = [
    {
        "name": "vendors",
        "description": "Operations with vendors.",
    },
    {
        "name": "products",
        "description": "Operations with products.",
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    version="0.0.1",
    contact={
        "name": "Ilya Kochankov",
        "email": "ilyakochankov@yandex.ru",
    },
    openapi_tags=tags_metadata,
    docs_url="/api/vendor/openapi",
    openapi_url="/api/vendor/openapi.json",
    default_response_class=ORJSONResponse,
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await db.start_db(settings.DB_URL)


@app.on_event("shutdown")
async def shutdown():
    await db.close_db()


def is_database_online(session: bool = Depends(db.get_db)):
    return session


app.include_router(vendor.router, prefix="/api/vendor/v1", tags=["vendors"])
app.include_router(product.router, prefix="/api/vendor/v1", tags=["products"])
app.add_api_route("/health", health([is_database_online]))

app.add_middleware(TrustedHostMiddleware, allowed_hosts=VENDOR_ALLOWED_HOSTS)

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_config=loger.LOGGING,
        log_level=logging.DEBUG,
    )

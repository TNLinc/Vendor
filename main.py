from logging.config import dictConfig

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi_health import health
from fastapi_pagination import add_pagination
from starlette.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

from api.v1 import product, vendor
from core import loger
from core.config import settings
import db
from core.loger import LOGGING

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

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)


def is_database_online(session: bool = Depends(db.create_session)):
    return session


app.include_router(vendor.router, prefix="/api/vendor/v1", tags=["vendors"])
app.include_router(product.router, prefix="/api/vendor/v1", tags=["products"])
app.add_api_route("/health", health([is_database_online]))

add_pagination(app)

dictConfig(LOGGING)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=settings.PORT,
        log_config=loger.LOGGING,
    )

from fastapi import FastAPI

from .routers import accounts
from .db.main import database


app = FastAPI(
    title="CostsMap",
    description="CostsMap is an application for costs accounting",
    version="3.0.0",
    contact={
        "name": "Artemowkin (main developer)",
        "url": "https://github.com/artemowkin/",
        "email": "artemowkin@yandex.ru",
    },
    license_info={
        "name": "GPL-3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html"
    },
    docs_url="/api/v1/auth/docs/",
    redoc_url="/api/v1/auth/redoc/",
)

app.include_router(accounts.router, prefix="/api/v1/auth", tags=["auth"])

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

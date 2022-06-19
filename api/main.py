from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine

from accounts.routes import router as accounts_router
from cards.routes import router as cards_router
from categories.routes import router as categories_router
from costs.routes import router as costs_router
from incomes.routes import router as incomes_router
from project.settings import config
from project.db import get_database, metadata


origins = ["*"]

app = FastAPI(
    title="CostsMap",
    description="CostsMap is an application for costs accounting",
    version="3.0.0",
    contact={
        "name": "Artemowkin (main developer)",
        "url": "https://github.com/artemowkin",
    },
    license_info={
        "name": "GPL-3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html"
    },
    docs_url="/api/v1/docs/",
    redoc_url="/api/v1/redoc/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)

app.include_router(accounts_router, prefix="/api/v1/auth", tags=["auth"])

app.include_router(cards_router, prefix="/api/v1/cards", tags=["cards"])

app.include_router(categories_router, prefix="/api/v1/categories", tags=["categories"])

app.include_router(costs_router, prefix="/api/v1/costs", tags=["costs"])

app.include_router(incomes_router, prefix="/api/v1/incomes", tags=["incomes"])


@app.on_event("startup")
def startup():
    engine = create_engine(config.database_url)
    metadata.create_all(engine)


@app.on_event("shutdown")
async def shutdown():
    db = await get_database()
    await db.disconnect()

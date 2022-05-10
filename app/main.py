from fastapi import FastAPI
import databases

from .routers import accounts, categories, cards, costs
from .settings import config


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
    docs_url="/api/v1/docs/",
    redoc_url="/api/v1/redoc/",
)

app.include_router(accounts.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(
    categories.router,
    prefix="/api/v1/categories",
    tags=["categories"]
)
app.include_router(cards.router, prefix="/api/v1/cards", tags=["cards"])
app.include_router(costs.router, prefix="/api/v1/costs", tags=["costs"])


@app.on_event("startup")
async def startup():
    if config.is_testing:
        config.database = databases.Database(config.test_db_url)
    else:
        config.database = databases.Database(config.database_url)

    await config.database.connect()


@app.on_event("shutdown")
async def shutdown():
    if not config.database: await config.database.disconnect()

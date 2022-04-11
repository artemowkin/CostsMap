from fastapi import FastAPI

from .routers import categories, costs, incomes, accounts
from app.db.main import database, metadata, engine


app = FastAPI(docs_url=None, redoc_url="/docs")

app.include_router(
    accounts.router, prefix="/api/v1/auth", tags=["authentication"]
)
app.include_router(
    categories.router, prefix="/api/v1/categories", tags=["categories"]
)
app.include_router(costs.router, prefix="/api/v1/costs", tags=["costs"])
app.include_router(incomes.router, prefix="/api/v1/incomes", tags=["incomes"])


@app.on_event('startup')
async def startup():
    await database.connect()
    metadata.create_all(engine)


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

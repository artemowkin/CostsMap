from fastapi import FastAPI

from .routers import accounts
from .db.main import database


app = FastAPI()

app.include_router(accounts.router, prefix="/api/v1/auth", tags=["auth"])

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

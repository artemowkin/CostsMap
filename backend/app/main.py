import asyncio
from argparse import ArgumentParser

from fastapi import FastAPI
from hypercorn.config import Config
from hypercorn.asyncio import serve

from .project.db import database, metadata
from .authentication.routes import router as authentication_router
from .categories.routes import router as categories_router
from .cards.routes import router as cards_router
from .costs.routes import router as costs_router


parser = ArgumentParser()

parser.add_argument('--host', type=str, default='0.0.0.0')

parser.add_argument('--port', type=int, default=8000)


app = FastAPI(title='CostsMap')

app.include_router(authentication_router, prefix='/api/auth', tags=['authentication'])

app.include_router(categories_router, prefix='/api/categories', tags=['categories'])

app.include_router(cards_router, prefix='/api/cards', tags=['cards'])

app.include_router(costs_router, prefix='/api/costs', tags=['costs'])


@app.on_event('startup')
async def on_startup():
    from .authentication.models import User
    from .categories.models import Category
    from .cards.models import Card
    from .costs.models import Cost
    metadata.create_all()
    await database.connect()


@app.on_event('shutdown')
async def on_shutdown():
    await database.disconnect()


def main():
    args = parser.parse_args()
    config = Config()
    config.bind = [f"{args.host}:{args.port}"]
    config.use_reloader = True
    asyncio.run(serve(app, config)) # type: ignore


if __name__ == '__main__':
    main()

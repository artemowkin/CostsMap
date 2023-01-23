from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


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
    uvicorn.run('app.main:app', host=args.host, port=args.port, reload=True)


if __name__ == '__main__':
    main()

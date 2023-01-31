from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .authentication.routes import router as authentication_router
from .categories.routes import router as categories_router
from .cards.routes import router as cards_router
from .costs.routes import router as costs_router
from .incomes.routes import router as incomes_router
from .project.db import Base, engine


parser = ArgumentParser()

parser.add_argument('--host', type=str, default='0.0.0.0')

parser.add_argument('--port', type=int, default=8000)


app = FastAPI(title='CostsMap')

app.include_router(authentication_router, prefix='/api/auth', tags=['authentication'])

app.include_router(categories_router, prefix='/api/categories', tags=['categories'])

app.include_router(cards_router, prefix='/api/cards', tags=['cards'])

app.include_router(costs_router, prefix='/api/costs', tags=['costs'])

app.include_router(incomes_router, prefix='/api/incomes', tags=['incomes'])


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event('startup')
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event('shutdown')
async def on_shutdown():
    await engine.dispose()


def main():
    args = parser.parse_args()
    uvicorn.run('app.main:app', host=args.host, port=args.port, reload=True)


if __name__ == '__main__':
    main()

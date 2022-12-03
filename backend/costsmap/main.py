from argparse import ArgumentParser
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .project.databases import database
from .project.databases import metadata, engine
from .authentication.dependencies import get_token_user
from .authentication.routes import router as authentication_router
from .categories.routes import router as categories_router


parser = ArgumentParser()

parser.add_argument('--host', default='0.0.0.0', type=str)

parser.add_argument('--port', default=8000, type=int)


origins = ['*']


app = FastAPI()

app.include_router(authentication_router, prefix='/api/auth', tags=['auth'])

app.include_router(
    categories_router, prefix='/api/categories', tags=['categories'],
    dependencies=[Depends(get_token_user)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def on_startup():
    from .authentication.models import users
    from .categories.models import categories
    await database.connect()


@app.on_event('shutdown')
async def on_shutdown():
    await database.disconnect()
    metadata.create_all(bind=engine)


def main():
    args = parser.parse_args()
    uvicorn.run('costsmap.main:app', host=args.host, port=args.port, reload=True)


if __name__ == '__main__':
    main()

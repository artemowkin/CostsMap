import asyncio
from argparse import ArgumentParser

from fastapi import FastAPI
from hypercorn.config import Config
from hypercorn.asyncio import serve

from .project.db import database, metadata


parser = ArgumentParser()

parser.add_argument('--host', type=str, default='0.0.0.0')

parser.add_argument('--port', type=int, default=8000)


app = FastAPI(title='CostsMap')


@app.on_event('startup')
async def on_startup():
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

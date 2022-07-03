# CostsMap REST API

RESTful API for CostsMap application

## Run

### Using Docker

To run this project using docker you need to execute the following commands in `backend` project directory:

```
docker-compose build
docker-compose up -d
```

### Using Python

To run this project using python you need to install:

- [`poetry`](https://python-poetry.org/docs/#installation)
- `python>=3.10`

Create `.env` file in `backend/costsmap/` directory with content like:

```
DATABASE_URL="sqlite:///db.sqlite"
SECRET_KEY="<secret_key>"
```

> You can generate secret key using `openssl rand -hex 32` command

And execute the following commands in `backend` project directory:

```
poetry install
poetry run dev
```

## Test

To run tests you need to run `pytest` command in `backend` project directory:

```
pytest
```

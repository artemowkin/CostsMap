# CostsMap API

CostsMap is a site for costs accounting. On this site you can add your
costs and incomes, sort them by category and see monthly statistic. This
branch is a site REST API

## Summary

  - [Getting Started](#getting-started)
  - [Runing the tests](#running-the-tests)
  - [Authors](#authors)
  - [License](#license)

## Getting Started

These instructions will get you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on how to deploy the project on a live system.

### Prerequisites

To install this project you need to have:

* `python-3.8`
* `pipenv`

### Installing

First, you need to install dependencies

```
$ pipenv install --dev
```

After that you need to create a `.env` file with the following content:

```
ENVIRONMENT=<development|production>
SECRET_KEY=<your_secret_key>
DEBUG=<1|0>
POSTGRES_NAME=<postgres_dbname>
POSTGRES_USER=<postgres_dbuser>
POSTGRES_PASSWORD=<postgres_dbuser_password>
POSTGRES_HOST=<postgres_dbhost>
POSTGRES_PORT=<postgres_dbport>
```

For example:

```
ENVIRONMENT=development
SECRET_KEY="qq&!mwvo2znv(t5^h$6w68*$@-c8-=ms_6efon6ntzwv@76txt"
DEBUG=1
POSTGRES_NAME=costsmap
POSTGRES_USER=django
POSTGRES_PASSWORD=django
POSTGRES_HOST=localhost
POSTGRES_PORT=""
```

And now you can run pipenv environment:

```
$ pipenv shell
```

## Running the tests

To run the tests you need to run the following command:

```
$ ./manage.py test
```

## Authors

* **Artemowkin** - https://github.com/artemowkin/

## License

This project is licensed under the [GPL-3.0](LICENSE) License - see
the [LICENSE](LICENSE) file for details

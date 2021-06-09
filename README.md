# CostsMap

CostsMap is a site for costs accounting. On this site you can add your
costs and incomes, sort them by category and see monthly statistic

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

* `docker`
* `docker-compose`

### Installing

First, you need to build the Docker image

```
$ docker-compose build
```

After that you need to up this image

```
$ docker-compose up -d
```

And apply all migrations

```
$ docker-compose run web python manage.py migrate
```

## Running the tests

If you want to run all tests you can use the following command:

```
$ docker-compose run web python manage.py test
```

If you want to run only functional tests you can use the following command:

```
$ docker-compose run web python manage.py test functional_tests
```

## Authors

* **Artemowkin** - https://github.com/artemowkin/

## License

This project is licensed under the [GPL-3.0](LICENSE) License - see
the [LICENSE](LICENSE) file for details

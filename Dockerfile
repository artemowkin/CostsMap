FROM python:3.9
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /code
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN pip install pipenv
RUN pipenv install --system --dev --ignore-pipfile
COPY . /code/
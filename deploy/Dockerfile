FROM python:3.12
ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY pyproject.toml poetry.lock /src/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . /src/

# Start from a base image
FROM python:3.11.3-slim-bullseye as build-image

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11.3-slim-bullseye

WORKDIR /code

COPY --from=build-image /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

ENV PORT 8080

CMD uvicorn src.asgi:app --host 0.0.0.0 --port $PORT
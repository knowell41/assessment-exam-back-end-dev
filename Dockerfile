FROM python:3.10-slim as wsgi-server

RUN apt update \
    && apt install -y --no-install-recommends python3-dev default-libmysqlclient-dev build-essential libpq-dev dos2unix \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=2.1.1


RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

RUN rm -rf .dockerignore \
  LICENSE \
  poetry.lock \
  poetry.toml \
  README.md

RUN dos2unix entrypoint.sh \
    && chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 8000

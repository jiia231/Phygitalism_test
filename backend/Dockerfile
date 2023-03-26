ARG PYTHON_VERSION=3.11

# Creating a base with shared environment variables
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# psycopg2 needs libpq
RUN apt update && apt install -y libpq5


FROM base as builder

RUN apt install -y build-essential libpq-dev

# Install Poetry
RUN python3 -m venv $POETRY_HOME && \
    $POETRY_HOME/bin/pip install poetry==${POETRY_VERSION}


WORKDIR $PYSETUP_PATH
COPY ./app/poetry.lock ./app/pyproject.toml ./
RUN poetry install --only main


FROM base as test

# Copying poetry and venv into image
COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $PYSETUP_PATH
RUN poetry install

COPY ./tests-start.sh /tests-start.sh
RUN chmod +x /tests-start.sh

COPY ./app /app
WORKDIR /app

CMD ["/tests-start.sh"]


# 'production' stage uses the clean 'base' stage and copyies
# in only our runtime deps that were installed in the 'builder-base'
FROM base as production

COPY --from=builder $VENV_PATH $VENV_PATH

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./app /app
WORKDIR /app

CMD ["/start.sh"]

# Dockerfile
# See: https://github.com/michael0liver/python-poetry-docker-example
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM python:3.8.1-slim as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# builder-base is used to build dependencies
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.1.12
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev  # respects


# 'production' stage uses the clean 'python-base' stage and copyies
# in only our runtime deps that were installed in the 'builder-base'
FROM python-base as production

COPY --from=builder-base $VENV_PATH $VENV_PATH

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY alembic.ini /ldc/
COPY ./alembic /ldc/alembic

COPY ./ldc /ldc/ldc

# Run migrations
WORKDIR /ldc
ENTRYPOINT /docker-entrypoint.sh $0 $@

WORKDIR /ldc/ldc
CMD [ "python", "bot.py" ]

FROM ubuntu:latest

COPY . /app

WORKDIR /app

RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
ARG DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    curl

# Install Python 3.11
RUN apt-get install build-essential dos2unix python3-full python3-dev libpq-dev -y

# Configure Poetry
ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.5.1

# System deps:
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies with poetry
RUN poetry install --no-root

# Startup
ENV FLASK_APP=plasticome_metadata.routes.app.py
CMD [ "flask", "run" , "-h", "0.0.0.0"]

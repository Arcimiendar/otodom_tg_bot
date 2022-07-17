FROM python:3.10-bullseye

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$PATH:$POETRY_HOME/bin"

RUN apt-get install curl -y
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

WORKDIR app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && poetry install

COPY ./src /app/
COPY urls_to_scrap.txt /app/

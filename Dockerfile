FROM python:3.8

WORKDIR /code

RUN pip install poetry

COPY pyproject.toml poetry.lock /code/

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . /code/

ARG PORT=$PORT

# Listen to server specified PORT
CMD ["uvicorn", "samudra.serve:app", "--port", PORT]
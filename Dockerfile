FROM python:3.8

WORKDIR /code

COPY ./poetry.lock /code/poetry.lock

RUN pip install poetry

RUN poetry install

COPY . /code/

CMD ["uvicorn", "samudra.serve:app"]
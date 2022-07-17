# Samudra

A simple dictionary web application.

## MVP Features

### Models

- Lemma (Lemma)
- Konsep (Concept)
- KataAsing (Foreign Word)
- Cakupan (Context of Meaning)

### Interactions

1. Add words with meaning. (DONE)
2. Add contexts to meaning. (DONE)
3. Add foreign words to meaning. (DONE)
4. Retrieve word and related information. (DONE)
5. Expose API using FastAPI. (DONE)

## Installation

1. Python 3.8 or later
2. Install [poetry](https://python-poetry.org/docs/)
3. `poetry install` (creating a virtual environment is recommended)

## Running the app

To run the app, either use `uvicorn samudra.main:app --reload` or `python ./samudra/main.py`
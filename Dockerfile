FROM python:3.13-slim

RUN pip install poetry

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-root

COPY . .
CMD ["poetry", "run", "python", "main.py"]

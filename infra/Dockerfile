FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m pip install --upgrade pip \
  && pip install -e ".[dev]"

CMD ["python", "-m", "src"]


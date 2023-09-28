FROM python:3.11.2-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --no-cache-dir poetry==1.5.1 \
    && poetry config virtualenvs.create false
COPY pyproject.toml /app
RUN poetry install --no-root ; mkdir logs
COPY . .
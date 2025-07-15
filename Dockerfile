# start from a small, official Python image
FROM python:3.11-slim

# prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# set working dir
WORKDIR /app

# install OS deps 
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc \
 && rm -rf /var/lib/apt/lists/*

# copy and install Python dependencies
COPY pyproject.toml poetry.lock* /app/
RUN pip install --upgrade pip \
 && pip install poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-dev --no-root

# copy your application code
COPY . /app

# expose the port FastAPI uses
EXPOSE 8000

# default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Dockerfile
FROM python:3.11-slim

# set a deterministic working directory
WORKDIR /app

# copy & install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# copy in the rest of your application
COPY . .

# expose the port uvicorn will run on
EXPOSE 8000

# default startup command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

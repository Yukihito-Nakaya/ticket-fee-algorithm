
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app/
COPY requirements.txt /app/
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt\
    && pip install pytz

COPY . /app/
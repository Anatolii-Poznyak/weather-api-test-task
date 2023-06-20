FROM python:3.11-slim-buster
LABEL maintainer="anatolii.pznk@gmail.com"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN groupadd -r celery && useradd -r -g celery celery
USER celery

COPY . /app/

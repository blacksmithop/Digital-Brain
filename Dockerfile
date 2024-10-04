FROM python:3.11-slim-bullseye

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

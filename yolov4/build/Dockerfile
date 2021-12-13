#syntax=docker/dockerfile:1
FROM python:3.9-slim-buster

# for PostgreSQL - libpq-dev
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  libopencv-dev \
  python3-opencv \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

COPY requirements.txt .

RUN python3.9 -m pip install --no-cache-dir --upgrade \
  pip \
  setuptools \
  wheel

RUN python3.9 -m pip install --no-cache-dir \
  -r requirements.txt

EXPOSE 5434

CMD ["python3", "./main.py"]

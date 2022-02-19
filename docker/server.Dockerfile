FROM python:3.8-slim

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip3 install Flask && \
    pip3 install flask-cors && \
    pip3 install waitress && \
    pip3 install redis && \
    pip3 install pycryptodome && \
    pip3 install celery

COPY ./server /app/server
COPY ./encryptor /app/encryptor
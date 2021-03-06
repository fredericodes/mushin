FROM python:3.9-slim

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    apt-get -y update && \
    apt-get -y install libmagic-dev && \
    pip3 install Flask && \
    pip3 install flask-cors && \
    pip3 install waitress && \
    pip3 install redis && \
    pip3 install pycryptodome && \
    pip3 install celery && \
    pip3 install Pillow && \
    pip3 install python-magic && \
    pip3 install eyeD3 && \
    pip3 install schedule

COPY ./server /app/server
COPY ./util /app/util
FROM python:3.8-slim

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip3 install Flask && \
    pip3 install flask-cors && \
    pip3 install pika && \
    pip3 install waitress

COPY ./server /app/server
COPY ./producer /app/producer

ENTRYPOINT [ "python3" ]
CMD [ "server/server.py" ]
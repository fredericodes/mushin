FROM python:3.8-slim

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip3 install Flask

COPY ./api /app

ENTRYPOINT [ "python3" ]
CMD [ "server/server.py" ]
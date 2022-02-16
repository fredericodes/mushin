FROM python:3.8-slim

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip3 install Flask && \
    pip3 install pika && \
    pip3 install waitress

COPY ./api /app

RUN chmod a+x ./api.sh

CMD [ "./api.sh" ]
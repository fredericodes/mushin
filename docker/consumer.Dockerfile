FROM python:3.8-slim

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip3 install pika &&

COPY ./consumer /app/consumer
COPY ./aes /app/aes

ENTRYPOINT [ "python3" ]
CMD [ "consumer/consumer.py" ]

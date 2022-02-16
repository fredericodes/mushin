FROM python:3.8-slim

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip3 install pika && \
    pip3 install pycryptodome && \
    pip3 install redis

COPY ./consumer /app/consumer
COPY ./encryptor /app/encryptor

ENTRYPOINT [ "python3" ]
CMD [ "consumer/consumer.py" ]

import codecs
import os
import sys
import redis
import requests
import pika

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

from encryptor.aes import encrypt_file

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq3',
                              credentials=pika.credentials.PlainCredentials("mushin_user", "mushin_pass")))
channel = connection.channel()

channel.queue_declare(queue='encryption_uploads', durable=True)


def callback(ch, method, properties, body):
    encoding = 'utf-8'
    file_tracking_id = body.decode(encoding)

    redis_instance = redis.Redis(host='redis', port=6379)
    file_name = redis_instance.get(file_tracking_id)
    get_uploaded_file_endpoint = 'http://localhost:10000/encryption/upload?fileName={}'.format(str(file_name))
    response = requests.get(get_uploaded_file_endpoint)
    status_code = response.headers['status_code']
    if status_code == '200':
        with codecs.open(str(file_name), 'wb') as f:
            f.write(response.content)
            private_secret_key = encrypt_file(file_name)
            if private_secret_key is not None:
                # TODO:
                # upload encrypted file to minio s3
                # remove encrypted file from this server if s3 upload success
                # remove original file from this server if s3 upload success
                # remove the original file from server 2 if s3 upload success
                ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='encryption_uploads', on_message_callback=callback)

channel.start_consuming()

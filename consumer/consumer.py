import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

import pika
from encryptor.aes import encrypt_file

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq3',
                              credentials=pika.credentials.PlainCredentials("mushin_user", "mushin_pass")))
channel = connection.channel()

channel.queue_declare(queue='encryption_uploads', durable=True)


def callback(ch, method, properties, body):
    encoding = 'utf-8'
    file_path = "../encrypt-uploads/" + body.decode(encoding)
    encrypt_file(file_path)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='encryption_uploads', on_message_callback=callback)

channel.start_consuming()
